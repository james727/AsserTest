import inspect, ast

def assert_tests( f ):
    tree = get_sanitized_ast( f ) # Get the AST

    # set up test counters
    test_counter_name, pass_counter_name = get_counter_names( f )
    add_variable_inits( tree, test_counter_name, pass_counter_name )

    # transform assert statements
    transformer = AssertTransformer( "num_tests", "num_passes" )
    transformer.visit( tree )

    # print results at the end
    add_print_statements( tree, test_counter_name, pass_counter_name, f.__name__ )

    myScope = {} # Create new namespace to compile tree in
    exec( compile( tree, '', 'exec' ), myScope, myScope )

    f.__code__ = myScope[ f.__name__ ].__code__
    return f

class AssertTransformer( ast.NodeTransformer ):
    # Transforms assert statements into try-except-finally blocks, with some logic to track the number of asserts that pass.
    def __init__( self, assert_counter_name, pass_counter_name ):
        self.test_counter = assert_counter_name
        self.pass_counter = pass_counter_name

    def visit_Assert( self, node ):
        # Converts assert statements into try-except-finally blocks that increment the relevant counters
        try_except_block = self.create_try_except_block( node )
        finally_block = self.create_finally_block( node )
        new_node = ast.TryFinally( body = try_except_block, finalbody = finally_block, nl = True )
        ast.fix_missing_locations( new_node )
        return new_node

    def create_try_block( self, node ):
        # Does the asserted action, then increments the passed test counter
        inc_statement = ast.AugAssign( target = ast.Name( id = self.pass_counter, ctx = ast.Store() ), op = ast.Add(), value = ast.Num( n = 1 ) )
        return [ node, inc_statement ]

    def create_except_block( self, node ):
        # Placeholder - to be updated to print failed tests
        # TODO: instead of pass, have it print details of failed test
        except_statement = ast.ExceptHandler( type = None, name = None, body = [ ast.Pass() ] )
        return [ except_statement ]

    def create_try_except_block( self, node ):
        # Creates the entire try except block
        try_body = self.create_try_block( node )
        except_body = self.create_except_block( node )
        try_except_statement = ast.TryExcept( body = try_body, handlers = except_body, orelse = [] )
        return [ try_except_statement ]

    def create_finally_block( self, node ):
        # Increments the total # of tests
        inc_statement = ast.AugAssign( target = ast.Name( id = self.test_counter, ctx = ast.Store() ), op = ast.Add(), value = ast.Num( n = 1 ) )
        return [ inc_statement ]

def get_sanitized_ast( f ):
    # Gets the AST for a function with decorators removed
    src = inspect.getsource( f ) # Get source code
    tree = ast.parse( src ) # Convert source to AST
    tree.body[0].decorator_list = [] # Remove decorator
    return tree

def get_counter_names( f ):
    # Generate counter names that don't conflict with local variables
    # TODO: update this to ensure lack of conflicts
    return "num_tests", "num_passes"

def add_variable_inits( tree, t, p ):
    # Update the AST to initialize counters to 0 with names t and p
    test_counter = ast.Assign( targets = [ ast.Name( id = t, ctx = ast.Store() ) ], value = ast.Num( n=0 ) )
    pass_counter = ast.Assign( targets = [ ast.Name( id = p, ctx = ast.Store() ) ], value = ast.Num( n=0 ) )
    current_function_body = tree.body[ 0 ].body
    tree.body[ 0 ].body = [ test_counter, pass_counter ] + current_function_body
    ast.fix_missing_locations( tree )

def add_print_statements( tree, t, p, func_name ):
    # Add print statements at end of function
    s = '==== {}: {}/{} tests passed ===='
    format_args = [ ast.Str( s = func_name ), ast.Name( id = p, ctx = ast.Load() ), ast.Name( id = t, ctx = ast.Load() ) ]
    formatted_string = ast.Attribute( value = ast.Str( s = s ), attr = 'format', ctx = ast.Load() )

    call_node = ast.Call( func = formatted_string, args = format_args, keywords = [], starargs = None, kwargs = None )

    print_node = ast.Print( dest = None, values = [ call_node ], nl = True )

    tree.body[ 0 ].body.append( print_node )
    ast.fix_missing_locations( tree )
