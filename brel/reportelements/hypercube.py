from brel import BrelLabel, QName
from brel.reportelements import IReportElement


class Hypercube(IReportElement):
    def __init__(self, name: QName, labels: list[BrelLabel]):
        self.__name = name
        self.__labels = labels

    def get_name(self) -> QName:
        """
        @return QName: the name of the hypercube as a QName
        """
        return self.__name

    def get_labels(self) -> list[BrelLabel]:
        """
        @return list[BrelLabel]: the labels of the hypercube
        """
        return self.__labels

    def _add_label(self, label: BrelLabel):
        """
        Add a label to the hypercube. This method is used by the parser and should not be used by the user.
        However, if you want to add a label to a hypercube, you can use this method.
        @param label: the label to add to the hypercube
        """
        self.__labels.append(label)

    def __str__(self) -> str:
        """
        @return str: the name of the hypercube as a string
        """
        return self.__name.__str__()
