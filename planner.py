from flight import Flight
import sys
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)
    def extract(self):
        return(self.items.pop(0))
def comp_1(x, y):
    return x[0] < y[0]

class Heap:
    def __init__(self, comparison_function, init_array=[]):
        self.comp = comparison_function
        self.heaplist = []
        for item in init_array:
            self.insert(item)

    def heapify(self, arr, n, i):
        lt = 2 * i + 1
        rt = 2 * i + 2
        small = i

        if lt < n and self.comp(arr[lt], arr[small]):
            small = lt

        if rt < n and self.comp(arr[rt], arr[small]):
            small = rt

        if small != i:
            arr[i], arr[small] = arr[small], arr[i]
            self.heapify(arr, n, small)

    def insert(self, value):
        self.heaplist.append(value)
        i = len(self.heaplist) - 1

        while i > 0 and self.comp(self.heaplist[i], self.heaplist[(i - 1) // 2]):
            self.heaplist[(i - 1) // 2], self.heaplist[i] = self.heaplist[i], self.heaplist[(i - 1) // 2]
            i = (i - 1) // 2

    def extract(self):
        if len(self.heaplist) == 0:
            return None

        self.heaplist[0], self.heaplist[-1] = self.heaplist[-1], self.heaplist[0]
        res = self.heaplist.pop()

        if len(self.heaplist) != 0:
            self.heapify(self.heaplist, len(self.heaplist), 0)

        return res

    def is_empty(self):
        return len(self.heaplist) == 0




    
class Planner:
    def __init__(self, flights):
        self.m=-1
        
        #n calculation
        self.n=-1
        for i in flights:
            self.n=max(self.n,i.start_city,i.end_city)
            self.m=max(self.m,i.flight_no)
        #adjacency list making for cities start 
        self.m+=1
        self.adj_l_c1=[[] for j in range(self.n+1)]
        for i in flights:
            self.adj_l_c1[i.start_city].append(i)
        #adjacency list making for cities end
        self.adj_l_c2=[[] for j in range(self.n+1)]
        for i in flights:
            self.adj_l_c2[i.end_city].append(i)
        #adjacency list making for flights
        self.adj_l_f=[[] for _ in range(self.m)]
        for i in flights:
            for j in self.adj_l_c2[i.start_city]:
                if((i.departure_time-j.arrival_time)>=20):
                    self.adj_l_f[j.flight_no].append(i)
       

    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        if(start_city==end_city):return []
        if(t1>t2):return []
        source_flights=[]
        for i in self.adj_l_c1[start_city]:
            if(i.departure_time>=t1):
                source_flights.append(i)
        
        opt_flightl=[]
        opt_distance=float('inf')
        def bfs(src_flight,adj,end,t2):#return distance and parent
            s=src_flight.flight_no
            parent=[None for _ in range(self.m)]
            visited=[0 for _ in range(self.m)]
            #p=2*self.m
            dist=[float('inf') for _ in range(self.m)]
            dist[s]=0
            q=Queue()        
            q.enqueue(src_flight)
            q.enqueue(None)
            visited[s]=1
            if(src_flight.end_city==end and src_flight.arrival_time<=t2):
                return[0,[src_flight]]
            fin_flight=None
            present_entered=[]
            while(not(q.size()==1)):
                
                u=q.extract()
                if(u!=None):
                    
                    for i in adj[u.flight_no]:
                        if(visited[i.flight_no]==0):                
                            dist[i.flight_no]=dist[u.flight_no]+1
                            visited[i.flight_no]=1
                            parent[i.flight_no]=u
                            q.enqueue(i)    
                            present_entered.append(i)
                else:
                    for j in present_entered:
                        #visited[j.flight_no]=1
                        if(j.end_city==end):  #check fare stored in dist
                            if(j.arrival_time<=t2):                            
                                if(fin_flight==None or j.arrival_time<fin_flight.arrival_time):
                                    fin_flight=j
                    present_entered=[]
                    q.enqueue(None)
                    if(fin_flight!=None):
                        break            
            
            if(fin_flight!=None):
                temp=fin_flight
                #print(fin_flight.arrival_time,212)
                res1=[temp]
                while (temp.flight_no!=s):
                    res1.append(parent[temp.flight_no])
                    temp=parent[temp.flight_no]
                
                res2=res1[::-1]
                return (dist[res2[-1].flight_no],res2)
            else:
                return None

       
        for i in source_flights:
            
            x=bfs(i,self.adj_l_f,end_city,t2)
            if(x==None):
                continue
            elif(x[0]<opt_distance):
                opt_distance=x[0]
                opt_flightl=x[1]
                #print(opt_flightl,opt_flightl[0].arrival_time,t2)
            elif(x[0]==opt_distance):
                if(len(opt_flightl)!=0 and (x[1][-1].arrival_time<opt_flightl[-1].arrival_time)):
                    opt_distance=x[0]
                    opt_flightl=x[1]
                    #print(opt_flightl,opt_flightl[0].arrival_time,t2)
        return(opt_flightl)

        


    
    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        if t1 > t2:
            return []

        source_flights = []
        for i in self.adj_l_c1[start_city]:
            if i.departure_time >= t1:
                source_flights.append(i)

        opt_flightl = []
        opt_cost = float('inf')

        def dikstra(source_flight, adj, end, t2):
            s = source_flight.flight_no
            finalised = [0 for _ in range(self.m)]
            cost = [float('inf') for _ in range(self.m)]
            parent = [None for _ in range(self.m)]
            cost[s] = source_flight.fare

            h = Heap(comp_1, [[cost[s], source_flight]])
            processed_nodes = []

            while not h.is_empty():
                node = h.extract()
                u = node[1]

                #if finalised[u.flight_no]:
                #    continue

                finalised[u.flight_no] = 1
                processed_nodes.append(u)

                # Traverse adjacent flights
                for i in adj[u.flight_no]:
                    if not finalised[i.flight_no]:
                        new_cost = cost[u.flight_no] + i.fare
                        if new_cost < cost[i.flight_no]:
                            cost[i.flight_no] = new_cost
                            parent[i.flight_no] = u
                            h.insert([new_cost, i])

            # After heap is empty, find the best valid flight among processed nodes
            fin_flight = None
            for u in processed_nodes:
                if u.end_city == end and u.arrival_time <= t2:
                    if fin_flight is None or cost[u.flight_no] < cost[fin_flight.flight_no]:
                        fin_flight = u
                    

            # Backtrace the path if we found a valid final flight
            if fin_flight is not None:
                temp = fin_flight
                res1 = [temp]
                while temp.flight_no != s:
                    res1.append(parent[temp.flight_no])
                    temp = parent[temp.flight_no]

                res2 = res1[::-1]
                return res2, cost[res2[-1].flight_no]  # Path and total cost
            else:
                return None

        # Iterate over all flights from the source city that depart on or after t1
        for flight in source_flights:
            result = dikstra(flight, self.adj_l_f, end_city, t2)
            if result is None:
                continue
            path, cost_of_path = result
            if cost_of_path < opt_cost:
                opt_flightl = path
                opt_cost = cost_of_path
            
        print(opt_flightl)
        print()
        return opt_flightl





    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if(start_city==end_city):return []
        if(t1>t2):return []
        source_flights=[]
        for i in self.adj_l_c1[start_city]:
            if(i.departure_time>=t1):
                source_flights.append(i)
        opt_flightl=[]
        opt_cost=float('inf')
        opt_distance=2*self.m+1
        def bfs(src_flight,adj,end,t2):#return distance and parent and fare
            s=src_flight.flight_no
            parent=[None for _ in range(self.m)]
            visited=[0 for _ in range(self.m)]
            dist=[float('inf') for _ in range(self.m)]
            cost=[float('inf') for _ in range(self.m)]
            dist[s]=0
            cost[s]=0

            q=Queue()        
            q.enqueue(src_flight)
            q.enqueue(None)
            visited[s]=1
            if(src_flight.end_city==end and src_flight.arrival_time<=t2):
                return[0,[src_flight],src_flight.fare]
            fin_flight=None
            present_entered=[]
            while(not(q.size()==1)):
                
                u=q.extract()
                if(u!=None):
                    
                    for i in adj[u.flight_no]:
                        if(visited[i.flight_no]==0):                
                            dist[i.flight_no]=dist[u.flight_no]+1
                            #visited[i.flight_no]=1
                            if((cost[u.flight_no]+u.fare)<cost[i.flight_no]):
                                parent[i.flight_no]=u
                                cost[i.flight_no]=cost[u.flight_no]+u.fare
                            q.enqueue(i)    
                            present_entered.append(i)
                else:
                    for j in present_entered:
                        visited[j.flight_no]=1
                        if(j.end_city==end):  #check fare stored in dist
                            if(j.arrival_time<=t2):                            
                                if((fin_flight==None) or (cost[j.flight_no]+j.fare)<(cost[fin_flight.flight_no]+fin_flight.fare)):
                                    fin_flight=j
                    present_entered=[]
                    q.enqueue(None)
                    if(fin_flight!=None):
                        break            
            
            if(fin_flight!=None):
                temp=fin_flight
                res1=[temp]
                while (temp.flight_no!=s):
                    res1.append(parent[temp.flight_no])
                    temp=parent[temp.flight_no]
                
                res2=res1[::-1]
                return (dist[res2[-1].flight_no],res2,cost[res2[-1].flight_no]+res2[-1].fare)
            else:
                return None


        for i in source_flights:
            x=bfs(i,self.adj_l_f,end_city,t2)
            if(x==None):
                continue
            elif(x[0]<opt_distance):
                opt_distance=x[0]
                opt_flightl=x[1]
                opt_cost=x[2]

            elif(x[0]==opt_distance):
                if(opt_cost>x[2]):
                    opt_distance=x[0]
                    opt_flightl=x[1]
                    opt_cost=x[2]
        return(opt_flightl)