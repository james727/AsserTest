from assertest import assert_tests

@assert_tests
def assertest_tests( x ):
    assert x == 5
    assert x % 2 == 0
    assert x + 2 == 4
    assert True
    assert False

assertest_tests( 2 )
