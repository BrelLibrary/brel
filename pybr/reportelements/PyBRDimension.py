from pybr import QName, PyBRLabel
from pybr.reportelements import IReportElement


class PyBRDimension(IReportElement):
    def __init__(self, name: QName, labels: list[PyBRLabel]) -> None:
        self.__name = name
        self.__labels = labels
    
    def get_name(self) -> QName:
        # TODO: write docstring
        return self.__name
    
    def get_labels(self) -> list[PyBRLabel]:
        # TODO: write docstring
        return self.__labels
    
    def is_explicit(self) -> bool:
        # TODO: implement
        raise NotImplementedError
    
    def get_type(self):
        # TODO: implement
        # this method only works if it is a typed dimension
        # in that case, it returns the QName of the type or some other representation of the type
        raise NotImplementedError
    
    def __str__(self) -> str:
        return self.__name.__str__()
