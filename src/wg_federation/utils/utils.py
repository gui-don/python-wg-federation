class Utils:
    """
    Contains reusable utility code.
    This class only contains short, static methods.
    """

    @staticmethod
    def classname(instance: object) -> str:
        """
        Display the class name of a given object instance
        :param instance: Instance to get the class from
        :return:
        """
        return f'{instance.__class__.__name__}♦'
