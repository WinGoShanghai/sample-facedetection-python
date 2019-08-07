#! /usr/bin/env python
# coding=utf-8
import os
import copy
from hiai import config

class HiAiConfigItem(object):
    '''
        AIConfigItem is a member of AIConfig, which is contained
        by two elements:
        name: config name
        value: config value
    '''
    def __init__(self, name='', value=''):
        self.__name = name
        self.__value = value

    def name(self):
        return self.__name

    def value(self):
        return self.__value

class HiAiConfig(object):
    '''
        AIConfig is a generate field used in graph_config.proto. It contains
        repeated AIConfig fields mentioned above.
    '''
    def __init__(self, ai_config_item):
        if (isinstance(ai_config_item, list)
        or isinstance(ai_config_item, HiAiConfigItem)):
            self._ai_config_item = ai_config_item
        else:
            self._ai_config_item = None

    def AiConfigItems(self):
        return self._ai_config_item

class MyGraph(object):
    def __init__(self, file_path):
        self.__config_list = read_graph_config(file_path)  # 解析配置文件，保存为一个由字典组成的列表
        self.__graph_id = None  # graph的id
        self.__priority = None  # graph的priority
        self.__engines = {}  # 保存graph中所有的engine节点的id和engine_name
        self.__connection = {}  # 保存engines间的连接信息

    def get_config_list(self):
        return self.__config_list

    # 获取graph_id
    def get_graph_id(self):
        return self.__config_list[0].get("graph_id")

    # 获取graph的priority
    def get_graph_priority(self):
        return self.__config_list[0].get("priority")

    # 获取所有的engine name
    def get_all_engines(self):
        for i in range(0, len(self.__config_list)):
            temp_engine_name = self.__config_list[i].get("engine_name")
            if temp_engine_name:
                temp_id = self.__config_list[i].get("id")
                self.__engines[temp_id] = temp_engine_name
        return self.__engines

    def get_connect_info(self):
        src_engine_id1 = self.__config_list[4].get('src_engine_id')
        src_engine_id2 = self.__config_list[5].get('src_engine_id')
        src_port_id1 = self.__config_list[4].get('src_port_id')
        src_port_id2 = self.__config_list[5].get('src_port_id')
        dst_engine_id1 = self.__config_list[4].get('target_engine_id')
        dst_engine_id2 = self.__config_list[5].get('target_engine_id')
        dst_port_id1 = self.__config_list[4].get('target_port_id')
        dst_port_id2 = self.__config_list[5].get('target_port_id')
        return [{"src_engine_id": src_engine_id1, "src_port_id": src_port_id1,
                 "dst_engine_id": dst_engine_id1, "dst_port_id": dst_port_id1},
                {"src_engine_id": src_engine_id2, "src_port_id": src_port_id2,
                 "dst_engine_id": dst_engine_id2, "dst_port_id": dst_port_id2}]

    def get_engine_config(self, engine_name):
        engine = MyEngine(engine_name, self.__config_list)
        return engine.get_engine_config()


class MyEngine(object):
    def __init__(self, engine_name, config_list):
        self.__engine_name = engine_name
        self.__config_list = config_list
        self.__ai_config_item_list = []
        self.__ai_config = None
        self.__ai_model = None
        self.__model_name = None

    # 根据属性名字获取属性值，以engine为单位
    def get_value_by_name(self, key):
        for i in range(0, len(self.__config_list)):
            if (self.__config_list[i].get("engine_name") == self.__engine_name):
                return self.__config_list[i].get(key)

    # 获取当前engine的engine_name
    def get_engine_name(self):
        return self.__engine_name

    # 获取EngineConfig对象，以engine为单位
    def get_engine_config(self):
        # 1 配置AIConfigItem项，组成list，传给AIConfig类
        self.__ai_config_item_list.append(HiAiConfigItem("path", self.get_value_by_name("path")))
        self.__ai_config_item_list.append(HiAiConfigItem("dataType", self.get_value_by_name("dataType")))
        self.__ai_config_item_list.append(HiAiConfigItem("data_source", self.get_value_by_name("data_source")))
        self.__ai_config_item_list.append(HiAiConfigItem("fps", self.get_value_by_name("fps")))
        self.__ai_config_item_list.append(HiAiConfigItem("image_format", self.get_value_by_name("image_format")))
        self.__ai_config_item_list.append(HiAiConfigItem("image_size", self.get_value_by_name("image_size")))
        self.__ai_config_item_list.append(HiAiConfigItem("meanOfG", self.get_value_by_name("meanOfG")))
        self.__ai_config_item_list.append(HiAiConfigItem("meanOfR", self.get_value_by_name("meanOfR")))
        self.__ai_config_item_list.append(HiAiConfigItem("batch", self.get_value_by_name("batch")))
        self.__ai_config_item_list.append(HiAiConfigItem("useAll", self.get_value_by_name("useAll")))
        self.__ai_config_item_list.append(HiAiConfigItem("randomNumber", self.get_value_by_name("randomNumber")))
        self.__ai_config_item_list.append(HiAiConfigItem("target", self.get_value_by_name("target")))

        self.__ai_config_item_list.append(HiAiConfigItem("model_path", self.get_value_by_name("model_path")))
        self.__ai_config_item_list.append(HiAiConfigItem("init_config", self.get_value_by_name("init_config")))
        self.__ai_config_item_list.append(HiAiConfigItem("passcode", self.get_value_by_name("passcode")))
        self.__ai_config_item_list.append(HiAiConfigItem("dump_list", self.get_value_by_name("dump_list")))
        self.__ai_config_item_list.append(
            HiAiConfigItem("dvpp_parapath", self.get_value_by_name("dvpp_parapath")))

        self.__ai_config_item_list.append(HiAiConfigItem("output_name", self.get_value_by_name("output_name")))
        self.__ai_config_item_list.append(HiAiConfigItem("Confidence", self.get_value_by_name("Confidence")))
        self.__ai_config_item_list.append(HiAiConfigItem("PresenterIp", self.get_value_by_name("PresenterIp")))
        self.__ai_config_item_list.append(
            HiAiConfigItem("PresenterPort", self.get_value_by_name("PresenterPort")))
        self.__ai_config_item_list.append(HiAiConfigItem("ChannelName", self.get_value_by_name("ChannelName")))
        self.__ai_config_item_list.append(HiAiConfigItem("path", self.get_value_by_name("path")))

        self.__ai_config = HiAiConfig(self.__ai_config_item_list)

        if self.get_value_by_name("model_path"):
            self.__model_name = os.path.basename(self.get_value_by_name("model_path"))
            self.__ai_model = config.AIModelDescription(name=self.__model_name,
                                                        path=self.get_value_by_name("model_path"))

        side = self.get_value_by_name("side")
        so_names = self.get_value_by_name("so_name")
        thread_num = self.get_value_by_name("thread_num")
        engine_id = self.get_value_by_name("id")
        ai_config = self.__ai_config
        ai_model = self.__ai_model

        my_engine_config = config.EngineConfig(engine_name=self.__engine_name,
                                               side=side,
                                               so_names=so_names,
                                               thread_num=thread_num,
                                               engine_id=engine_id,
                                               ai_config=ai_config,
                                               ai_model=ai_model)
        return my_engine_config, ai_config


def read_graph_config(filepath):
    graph_dict = {}
    engines_list = []
    engine_dict = {}

    num_of_left = 0  # 左括号数
    num_of_right = 0  # 右括号数
    line_num = 0
    chazhi_num = 0  # 左括号减去右括号的差值
    temp_item = [0, 0]
    # 打开并读取文件
    f = open(filepath, 'r')
    lines = f.readlines()

    for line in lines:
        line_num = line_num + 1
        line = line.strip()  # 去除空格
        if not (len(line) or line.startswith('#')):  # 去除空行和注释行
            continue
        if line.__contains__('{'):
            num_of_left = num_of_left + 1
            line_split = line.split('{')
        if line.__contains__('}'):
            num_of_right = num_of_right + 1
            line_split = line.split('}')
        if line.__contains__(':'):
            line_split = line.split(':')

        for i in range(0, len(line_split)):
            line_split[i] = line_split[i].strip()
            if line_split[i] != "":
                line_split[i] = line_split[i].strip('"')

        if "" in line_split:
            line_split.remove("")

        if chazhi_num != 0:
            if (line.__contains__(':')) and (line_split[0] != 'name') and (line_split[0] != 'value'):
                engine_dict[line_split[0]] = line_split[1]
            elif line.__contains__('engines'):
                chazhi_num = 0
                # print(engine_dict)
            elif line_split[0] == 'name' and len(line_split) >= 2:
                temp_item[0] = line_split[1]
                engine_dict[temp_item[0]] = temp_item[1]
            elif line_split[0] == 'value' and len(line_split) >= 2:
                temp_item[1] = line_split[1]
                engine_dict[temp_item[0]] = temp_item[1]

        if num_of_left - num_of_right == 1:  # 保存graph的参数
            if len(line_split) == 2:
                graph_dict[str(line_split[0])] = line_split[1]

        if (line_split[0] == "engines") or (line_split[0] == "connects"):
            if engine_dict:
                engines_list.append(copy.deepcopy(engine_dict))
                engine_dict.clear()
        if (line_split[0] == "engines"):  # 需要优化
            chazhi_num = num_of_left - num_of_right
    engines_list.append(copy.deepcopy(engine_dict))
    engine_dict.clear()
    engines_list.insert(0, graph_dict)
    f.close()
    return engines_list


def parse_graph_config(config_file):
    graph = MyGraph(config_file)
    engine_configs = []
    for engine_id, engine_name in graph.get_all_engines().items():
        eng_conf, ai_conf = graph.get_engine_config(engine_name)
        cfg = (eng_conf, ai_conf)
        engine_configs.append(cfg)
    return engine_configs
