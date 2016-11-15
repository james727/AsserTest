from assertest import assert_tests

@assert_tests
def tests( x ):
    assert 5 == 5
    assert 4 == 1
    assert 2 == 2
    assert True

tests( 2 )
