class XPathExpression:
    def __init__(self, expression: str) -> None:
        self.__expression = expression

    def get_expression(self) -> str:
        return self.__expression
