import secrets

class MyRandom:
    def __init__(self, memory_seeds=None, comment_display=False):
        self.memory_seeds = memory_seeds if memory_seeds is not None else {}
        self.comment_display = comment_display
    
    def comments(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            if self.comment_display:
                all_args = list(args)
                if kwargs:
                    all_args.append(kwargs)
                
                class_name = self.__class__.__name__
                method_name = func.__name__
                
                print(f"Method {class_name}.{method_name}({all_args}) called.")
                if result is not None:
                    print(f"-> Result: {result}\n")
            
            return result
        return wrapper

    @comments
    def random(self, bits=1):
        return bin(secrets.randbits(bits))[2:].zfill(bits)

    @comments
    def seed(self, memory_cell, limit=2**16 - 1):
        self.memory_seeds[memory_cell] = self.random(10)

my_random = MyRandom(comment_display=True)
x = my_random.random(1)
my_random.seed(5, limit=100)
