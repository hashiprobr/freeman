graph [
  width 250
  height 250
  node_size 10
  node_color "rgb(0, 0, 0)"
  node_labpos "top right"
  node [
    id "A"
    x 0
    y 0
  ]
  node [
    id "B"
    x 0
    y 1
  ]
  node [
    id "C"
    x 1
    y 0
  ]
  node [
    id "D"
    x 0
    y -1
  ]
  node [
    id "E"
    x -1
    y 0
  ]
  edge [
    source "A"
    target "B"
  ]
  edge [
    source "A"
    target "C"
  ]
  edge [
    source "A"
    target "D"
  ]
  edge [
    source "A"
    target "E"
  ]
]
