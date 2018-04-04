# Dijkstra Algorithm
# 孙逸飞 11510170
def dijkstra(graph,src):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]  # 获取图中所有节点
    for i in range(len(graph)):
        distance = {} # 一维字典，源点到各节点最短路径
        path = {} # 二维字典，源点到各节点最短路径(倒序)
        forwarding_table = {} # 一维字典，源点到各节点最短路径的 源点路由方向
        D = {} # 一维字典，各节点到当前计算节点的最短路径的距离
        p = {} # 一维字典，各节点到当前计算节点的最短路径的前个节点名称
        N = {} # 一维字典，已知最短路径的节点名称

    ## Init.
    N[0] = src
    for node in range(len(graph)):
        if graph[src][node] != float('inf'):
            D[node] = graph[src][node]
            p[node] = src
        else:
            D[node] = float('inf')
    ## Loop
    for step in range(len(nodes)-1):
        #print(D.values()) # 调试用，可显示计算过程
        for d_idx in range(len(graph)):
            dm = float('inf');
            if D[d_idx]<dm and d_idx not in N.values():
                dm = D[d_idx]
                dm_idx = d_idx
        N[len(N)] = dm_idx
        cur_node = dm_idx
        for node in range(len(graph)):
            if graph[cur_node][node] != float('inf') and node not in N.values():
                 if D[cur_node] + graph[cur_node][node] < D[node]:
                    D[node] = D[cur_node] + graph[cur_node][node]
                    p[node] = cur_node

    ## 输出参数处理
    #distance
    distance = D
    for node in range(len(graph)):
        #path
        path[node] = {}
        path[node][0] = node
        while path[node][len(path[node])-1] is not src:
            path[node][len(path[node])] = p[path[node][len(path[node])-1]]
        # forwarding table
        if node is not src:  # 去掉源点到源点的情况
            forwarding_table[node] = path[node][len(path[node])-2]
        else:
            forwarding_table[src] = src

    return distance, path, forwarding_table

if __name__ == '__main__':
    graph_list = [[0, 7, float('inf'), 3, 3, 2],
                  [7, 0, 5, float('inf'), 1, 2],
                  [float('inf'), 5, 0, 6, float('inf'), 3],
                  [3, float('inf'), 6, 0, float('inf'), 1],
                  [3, 1, float('inf'), float('inf'), 0, float('inf')],
                  [2, 2, 3, 1, float('inf'), 0]]
    src = 3

    distance, path, forwarding_table = dijkstra(graph_list, src)  # 查找从源点3开始到其他节点的最短路径

    ## 打印从源点到各节点的最短路径距离
    print("Min Distance:")
    for node in range(len(graph_list)):
        if node is not src:  # 去掉源点到源点的情况
            print("%s->%s: %s" % (src, node, distance[node]))
    print()

    ## 打印从源点到各节点的路径
    print("Min Path:")
    for node in range(len(graph_list)):
        if node is not src:  # 去掉源点到源点的情况
            print("%s->%s: " % (src, node), end="")
            for node2 in range(len(path[node])):  # 将path倒序打印
                print("%s " % path[node][len(path[node]) - 1 - node2], end="")
            print()
    print()

    ## 打印源点的forwarding table
    print("Forwarding Table for src %s" % src)
    print("%5s|%5s" % ("Dest.", "Link"))
    for node in range(len(graph_list)):
        if node is not src:  # 去掉源点到源点的情况
            print("%5s|(%s,%s)" % (node, src, forwarding_table[node]))
    print()
    #print(distance)
    #print(path)
    #print(forwarding_table)
