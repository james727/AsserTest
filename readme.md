#AsserTest
For small projects I tend to just write a bunch of assert statements for tests, like this:

```python
def test_f():
  assert f( input1 ) == output1
  assert f( input2 ) == output2
  assert f( input3 ) == output3
  assert f( input4 ) == output4
  assert f( input5 ) == output5
```

AsserTest is a decorator that replaces all assert statements with `Try-Except-Finally` blocks and tells you how many of your assert statements passed. Running the following code:

```python
from assertest import assert_tests

@assert_tests
def assertest_tests( x ):
    assert x == 5
    assert x % 2 == 0
    assert x + 2 == 4
    assert True
    assert False

assertest_tests( 2 )
```

Will print the following to your terminal:

```
==== assertest_tests: 3/5 tests passed ====
```

### How it works
This works by manipulating the AST of the function the decorator is applied to.

### Todo
This is still a work in progress - the main thing I'd like to add is printing some details on failed tests
