def A1F2(rule, graph, raw_data, db_config, update_fdr_sql, irule_table, insert_immedres_sql, immed_result_table):
    """恒值点检查功能模块，多变量规则"""
    neo4j_id = rule[1]
    # 创建节点匹配器对象
    node_matcher = NodeMatcher(graph)
    # 创建关系匹配器对象，用于在图数据库中查找结点之间的边关系
    rel_matcher = RelationshipMatcher(graph)
    try:
        # 获取故障名称结点
        fault_name_node = node_matcher[neo4j_id]
        # 从该节点获取即时诊断连续恒值次数参数值，  可能表示多少次连续恒值就报警
        icons_series_num = int(fault_name_node['即时诊断连续恒值次数'])
        # 获取与该故障相关的输入变量节点的关系
        input_variables = list(rel_matcher.match([fault_name_node], r_type=level_4[0]))
        # 在rule_graph图中查找标签为level_3,name为。。。的第一个节点
        rule_fault_name_node = NodeMatcher(rule_graph).match(level_3, name=fault_name_node['name'].split('_')[-1]).first()
        # 在rule_graph图中的关系匹配对象中查找与rule_fault_name_node结点相关的关系类型为level_4的输入变量的关系
        rule_input_variables = list(RelationshipMatcher(rule_graph).match([rule_fault_name_node], r_type=level_4[0]))  
        
        #遍历输入变量，找到“非运行状态"的关键词，保存”报警“等关键状态标志
        enabled = 1
        keyword_list, name_dict = [], {}
        for input_variable in rule_input_variables:
            if input_variable.end_node['关键词'] != '["运行", "状态"]':
                # 找到每条故障内容中不为运行状态的节点
                rule_keyword = input_variable.end_node['关键词']
        # 创建输入变量的关键词列表，name_dict为变量名及对应的关键词
        for input_variable in input_variables:
            keyword_list.append(input_variable.end_node['关键词'])
            name_dict[input_variable.end_node['name']] = input_variable.end_node['关键词']
        #other_keywords是找到那些符合模板规则中的关键词的输入变量，即不是”运行“，”状态“的关键词
        other_keywords = [sublist for sublist in keyword_list if sublist==rule_keyword]
        #on_keywords是其余的关键词变量
        on_keywords = [sublist for sublist in keyword_list if sublist not in other_keywords]
        # 根据raw_data的列创建一个新的DataFrame
        diag_or_not = pd.DataFrame(columns=raw_data.columns)
        on_pv, other_pv = '', ''
        for key, value in name_dict.items():
            if value in other_keywords:
                # 先找到最关键的输入，如果在数据库没有该点的值，则确认因字段无效无法诊断。
                other_df = raw_data[(raw_data['pvvarname']==key)&(raw_data['enabled']==1)] # 存在该点且为启动状态的所有数据
                # 保存诊断的最关键的点，以及该点的相关数据
                if not other_df.empty:
                    other_pv = key
                    diag_or_not = pd.concat([diag_or_not, other_df], axis=0)
                    break
        other_pv = key if other_pv == '' else other_pv
        if diag_or_not.empty:
            enabled = 0
        else:
            for key, value in name_dict.items():