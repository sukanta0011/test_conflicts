try:
    int("a")
except Exception as e:
    print(f"{type(e).__name__}")


class Animal:
    def sound(self):
        print("General animal sound")


class Dog(Animal):
    def sound(self):
        print("Dog Sound")
        super().sound()


if __name__ == "__main__":
    dog = Dog()
    dog.sound()