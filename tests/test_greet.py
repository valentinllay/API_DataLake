from hello_world.greet import say_hello_world

def test_say_hello_world():
    # plain assert is enough
    assert say_hello_world() == "Hello world !"
