# -*- coding: UTF-8 -*-
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.cElementTree as ET

from xml.etree.ElementTree import ElementTree, Element

unique_id = 1


class XmlReader():
    # def __init__(self):
    def walkData(self, root_node, level, result_list):
        global unique_id
        temp_list = [unique_id, level, root_node.tag, root_node.attrib, root_node.text]
        result_list.append(temp_list)
        unique_id += 1

        # 遍历每个子节点
        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            self.walkData(child, level + 1, result_list)
        return

    def getXmlData(self, file_name):
        level = 1  # 节点的深度从1开始
        result_list = []
        root = ET.parse(file_name).getroot()
        self.walkData(root, level, result_list)

        return result_list

    def if_match(self, node, kv_map):

        """
        判断某个节点是否包含所传入的参数属性
        :param node: 节点
        :param kv_map: 属性及属性值组成的map
        """
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    def get_node_by_keyvalue(self, nodelist, kv_map):
        result_list = []
        for node in nodelist:
            if self.if_match(node, kv_map):
                result_list.append(node)
        return result_list

    def getModule(self):
        filename = os.getcwd() + r'\testcase_list.xml'
        caselist = []

        tree = ElementTree()
        tree.parse(filename)

        nodes = tree.findall("testsuit")
        # module_node = self.get_node_by_keyvalue(nodes, {"testclass": modulename})

        for node in nodes:
            for elem in node.iter():
                print elem.attrib
                if len(elem.attrib) == 3 :
                    caselist.append(elem.attrib["caseClass"])
                # else:
                #     print elem.attrib
        return caselist


