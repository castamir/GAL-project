import Components
import Magic

# dfs (graf(V,H))
# for u in V
#   color[u] = white
#   predek = NULL
# for u in V
#   if color[u] == white
#      dfs_visit(u)

# dfs_visit(u)
#   color = gray
#   for v in adj[u]
#     if color[v]  == white
#       predek += u
#       dfs_visit(v)
#     else
#       pole.add(v)
#       find_cycle(v, v)
#   color[u] = black
#
# find_cycle(u, v)
#  cycles = 0
#  pole.add(u)
#  for p in predek[u]
#    if(p == v) { # detekovana smycka
#       cycles++
#       prekopiruj pole do cilove matice smycek
#    }
#    else if (cycles = find_cycle(p,v))
#    if (cycles == 0)# nenasla se smycka
#
#  return cycles

def DFS(V, E):
    return

def DFS_Visit(u, v):
    return

def find_cycle(u, v):
    return