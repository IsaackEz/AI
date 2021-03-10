# **Branch and Bound**

It works similar to backtracking trying to find the tour at the minium cost

## **GRAPH**

      G.add_edge("A", "B")
      G.add_edge("A", "C")
      G.add_edge("A", "D")
      G.add_edge("A", "E")
      G.add_edge("B", "C")
      G.add_edge("B", "D")
      G.add_edge("B", "E")
      G.add_edge("C", "D")
      G.add_edge("C", "E")
      G.add_edge("D", "E")
      G.add_edge("E", "D")

## **Adjacency Matrix**

      [infinite, 20, 30, 10, 11],
      [15, infinite, 16, 4, 2],
      [3, 5, infinite, 2, 4],
      [19, 6, 18, infinite, 3],
      [16, 4, 7, 16, infinite],

## **REDUX**

It is necessary to reduce the matrix according to the transfer that will be made, this is achieved by changing the values of the matrix of the participating nodes by infinity.

## **BnB**

It determinates if the matrix has been reduced, it is necessary to consult in each row and column if there is a value equal to 0 or infinity without taking into account the values of the route that is being followed. With the new values in the columns and rows the value of _b_ is determined _b_ is a variable we got to use later.
