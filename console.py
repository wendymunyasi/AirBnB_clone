#!/usr/bin/python3
"""Contains the entry point of the command interpreter.

You must use the module cmd.
Your class definition must be: class HBNBCommand(cmd.Cmd):
Your command interpreter should implement:
quit and EOF to exit the program,
help (this action is provided by default by cmd but you should keep it
updated and documented as you work through tasks),
a custom prompt: (hbnb),
an empty line + ENTER shouldn’t execute anything.
Your code should not be executed when imported
"""
import cmd
import models
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """class for command processor.

    Args:
        cmd (_type_): _description_
    """
    prompt = "(hbnb) "
    classes_list = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]

    def do_quit(self, args):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, args):
        """EOF command to exit the program
        """
        return True

    def emptyline(self):
        """Empty line shouldn't execute anything
        """
        pass

    def do_create(self, inp):
        """Creates a new instance of BaseModel, saves it (to the JSON
        file) and prints the id.

        Args:
            class_name (class): name of current class.
        """
        args = inp.split()
        if not self.class_verification(args):
            return

        inst = eval(str(args[0]) + '()')
        if not isinstance(inst, BaseModel):
            return
        inst.save()
        print(inst.id)

    def do_show(self, inp):
        """Prints the string representation of an instance based on the
        class name and id.
        """
        args = inp.split()

        if not self.class_verification(args):
            return

        if not self.id_verification(args):
            return

        string_key = str(args[0]) + '.' + str(args[1])
        objects = models.storage.all()
        print(objects[string_key])

    @classmethod
    def class_verification(cls, args):
        """Verifies class and checks if it is in the class list.

        Returns:
            bool: True or false depending on status of class.
        """
        if len(args) == 0:
            print("** class name missing **")
            return False

        if args[0] not in cls.classes_list:
            print("** class doesn't exist **")
            return False

        return True

    @staticmethod
    def id_verification(args):
        """Verifies id of class.

        Returns:
            bool: True or False depending on status of id.
        """
        if len(args) < 2:
            print("** instance id missing **")
            return False

        objects = models.storage.all()
        string_key = str(args[0]) + '.' + str(args[1])
        if string_key not in objects.keys():
            print("** no instance found **")
            return False

        return True

    def do_destroy(self, inp):
        """Deletes an instance based on the class name and id (save the
        change into the JSON file).
        """
        args = inp.split()
        if not self.class_verification(args):
            return
        if not self.id_verification(args):
            return
        string_key = str(args[0]) + '.' + str(args[1])
        objects = models.storage.all()
        models.storage.delete(objects[string_key])
        models.storage.save()

    def do_all(self, inp):
        """Prints all string representation of all instances based or not
        on the class name.
        """
        args = inp.split()
        all_objects = models.storage.all()
        list_ = []
        if len(args) == 0:
            # print all classes
            for value in all_objects.values():
                list_.append(str(value))
        elif args[0] in self.classes_list:
            # print just arg[0] class instances
            for (key, value) in all_objects.items():
                if args[0] in key:
                    list_.append(str(value))
        else:
            print("** class doesn't exist **")
            return False
        print(list_)

    def do_update(self, line):
        """ Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """
        args = shlex.split(line)
        if not self.class_verification(args):
            return
        if not self.id_verification(args):
            return
        if not self.attribute_verification(args):
            return
        string_key = str(args[0]) + '.' + str(args[1])
        all_objects = models.storage.all()
        my_dict = all_objects[string_key].to_dict()
        attr_name = args[2]
        attr_value = args[3]
        for (key, value) in my_dict.items():
            try:
                if attr_name in key:
                    obj_dir = all_objects[string_key].__dir__()
                    if key in obj_dir:
                        val_c_attr = obj_dir[obj_dir.index(key)]
                        obj = eval('objects[string_key].__class__.' +
                                   val_c_attr)
                        if type(obj) is list:
                            print('converting list')
                            attr_value = eval(attr_value,
                                              {'__builtins__': None}, {})
                        else:
                            attr_value = obj.__class__(attr_value)
            except Exception:
                return
        setattr(all_objects[string_key], attr_name, attr_value)
        all_objects[string_key].save()

    @staticmethod
    def attribute_verification(args):
        """Verifies attributes.
        """
        if len(args) < 3:
            print("** attribute name missing **")
            return False
        if len(args) < 4:
            print("** value missing **")
            return False
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
