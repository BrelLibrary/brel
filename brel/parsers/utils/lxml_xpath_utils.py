import lxml.etree

def add_xpath_functions():
    
    def lower_case(context, s):
        return s.lower()
    
    def ends_with(context, s, suffix):
        return s.endswith(suffix)
    
    def tag_like(context, pattern):
        actual_tag = context.context_node.tag.lower()
        pattern = pattern.lower()
        return actual_tag.endswith(pattern)
    
    ns = lxml.etree.FunctionNamespace(None)
    ns['lower-case'] = lower_case
    ns['ends-with'] = ends_with
    ns['tag-like'] = tag_like

        
    
