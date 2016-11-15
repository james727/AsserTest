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

This is certainly not an optimal testing practice. AsserTest tries to make it slightly more robust.

## What it does
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
======== Testing assertest_tests ========

_______________ Failures _______________

Function line 1:
 >	assert x == 5

Function line 5:
 >	assert False

==== assertest_tests: 3/5 tests passed ====
```

Note that it will print one of the above statements for each function you apply the decorator to.

## Todo
This is still a work in progress - the main thing I'm working on is printing details on failed tests (i.e., actually evaluating each side of any comparison operator a la pytest). The logic for initializing the counter variables also needs to be built in to avoid local conflicts.
