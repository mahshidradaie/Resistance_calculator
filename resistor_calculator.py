def gauss_jordan(m, eps = 1.0/(10**10)):
  (h, w) = (len(m), len(m[0]))
  for y in range(0, h):
    maxrow = y
    for y2 in range(y+1, h):
      if abs(m[y2][y]) > abs(m[maxrow][y]):
        maxrow = y2
    (m[y], m[maxrow]) = (m[maxrow], m[y])
    if abs(m[y][y]) <= eps:
      return False
    for y2 in range(y+1, h):
      c = m[y2][y] / m[y][y]
      for x in range(y, w):
        m[y2][x] -= m[y][x] * c
  for y in range(h-1, 0-1, -1):
    c  = m[y][y]
    for y2 in range(0,y):
      for x in range(w-1, y-1, -1):
        m[y2][x] -=  m[y][x] * m[y2][y] / c
    m[y][y] /= c
    for x in range(h, w):
      m[y][x] /= c
  return True

def preprocess (indeps ,currents ,voltages):
    list_indep = []
    for i in range(len(indeps)): list_indep.append([])
    for fro, to, res in indeps:
        list_indep[fro].append((to, res))
        list_indep[to].append((fro, res))
    dep_C = []
    dep_V = []
    for fro,to, src, des, a, b in currents:
        dep_C.append((fro, to, src, des, a, b))
        dep_C.append((to, fro, src, des, -1 * a, -1 * b))
    for fro, to, src, des, a, b in voltages:
        dep_V.append((fro, to, src, des, a, b))
        dep_V.append((to ,fro,src, des, -1 * a, -1 * b))
    return list_indep, dep_C, dep_V

def make_eqns (list_indep, currents, voltages , node1, node2, nodes):
    coeffs = []
    Vars = nodes
    for i in range(Vars):
        cs = [0.0] * Vars
        if (i < len(list_indep)):
            cs[i] = sum(1 / b for (a, b) in list_indep[i])
            for other, res in list_indep[i]:
                cs[other] -= 1.0 / res
        for l in currents: #l= (node1, node2, src, dest, a, b)
            if i == l[0]: # to find the equation for node i
                 for j in range(len(list_indep[i])):
                     if list_indep[i][j][0] == l[1]: #to find the branch in order to use the resistance in that branch
                        #print (1/list_indep[i][j][1])
                        temp = (l[4] * (1 / list_indep[i][j][1]) + l[5]) #ith voltage is changed due to the given equation divided by the resistance in that branch
                        break
                 cs[l[2]] += temp
                 cs[l[3]] -= temp
        for l in voltages:
            if i == l[0]:
                for j in range(len(list_indep[i])):
                    if list_indep[i][j][0] == l[1]:
                        temp = l[4] * (1 / list_indep[i][j][1]) + l[5]
                        break
                cs[l[2]] -= temp
                cs[l[3]] += temp
        coeffs.append(cs)
    rhs = [0] * Vars
    rhs[node1] = 1.0
    rhs[node2] = -1.0
    n = max(node1, node2)
    coeffs = [c[:n] + c[n + 1:] for c in coeffs]
    return coeffs[:-1], rhs[:-1]

def calculate_resistance(indeps, currents, voltages, port, nodes):
    src = int(port[0])
    dst = int(port[1])
    list_indep, dep_C, dep_V = preprocess(indeps, currents, voltages)
    a, b = make_eqns(list_indep, dep_C,dep_V, src, dst, nodes)
    M = [a[i] + [b[i]] for i in range(len(a))]
    gauss_jordan(M)
    return abs(M[min(src, dst)][-1])

def Scanner():
    nodes = input("Enter the number of nodes: ")
    independent = int(input ("Enter the number of edges containing resistor only: "))
    indeps = []
    for i in range(independent):
        temp = []
        a, b, c = input ("edge \"node1 node2 resistance\": ").split()
        temp.append(int(a)), temp.append(int(b)), temp.append(int(c))
        indeps.append(temp)
    dependent = int (input("Enter the number of edges containing dependent sources: "))
    currents = []
    voltages = []
    for i in range(dependent):
        var_name = input("write \"i\" for current source and \"v\" for voltage source: ")
        if "i" in var_name:
            temp = []
            a, b = input("The dependent source is between nodes: ").split()
            temp.append(int(a))
            temp.append(int(b))  # this shows the branch containing that current
            a, b = input("It's the current between nodes: ").split()
            temp.append(int(a))
            temp.append(int(b))  # this shows the branch containing the dependent source
            print("Now, for the linear equation ai + b: ")
            temp.append(int(input("a: ")))
            temp.append(int(input("b: ")))
            currents.append(temp)
        elif "v" in var_name:
            temp = []
            a, b = input("The dependent source is between nodes: ").split()
            temp.append(int(a))
            temp.append(int(b))
            a, b = input("It's the voltage between nodes: ").split()
            temp.append(int(a))
            temp.append(int(b))
            print("Now, for the linear equation av + b: ")
            temp.append(float(input("a: ")))
            temp.append(float(input("b: ")))
            voltages.append(temp)
    src = input("choose source node: ")
    dest = input("choose destination node: ")
    port = [src, dest]
    return port, indeps, currents, voltages, nodes

if __name__ == '__main__':
    port, indeps, currents, voltages, nodes = Scanner()
    print (calculate_resistance(indeps, currents, voltages, port, int(nodes)))
