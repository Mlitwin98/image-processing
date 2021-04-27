from numpy import array

mask_sharp1 = array([[ 0,-1, 0],
                    [-1, 5,-1],
                    [ 0,-1, 0]])

mask_sharp2 = array([[-1,-1,-1],
                    [-1, 9,-1],
                    [-1,-1,-1]])

mask_sharp3 = array([[ 1,-2, 1],
                    [-2, 5,-2],
                    [ 1,-2, 1]])

mask_prewittN = array([[1,1,1],
                        [0,0,0],
                        [-1,-1,-1]])

mask_prewittNE = array([[0,1,1],
                        [-1,0,1],
                        [-1,-1,0]])

mask_prewittE = array([[-1,0,1],
                        [-1,0,1],
                        [-1,0,1]])

mask_prewittSE = array([[-1,-1,0],
                        [-1,0,1],
                        [0,1,1]])

mask_prewittS = array([[-1,-1,-1],
                        [0,0,0],
                        [1,1,1]])

mask_prewittSW = array([[0,-1,-1],
                        [1,0,-1],
                        [1,1,0]])

mask_prewittW = array([[1,0,-1],
                        [1,0,-1],
                        [1,0,-1]])

mask_prewittNW = array([[1,1,0],
                        [1,0,-1],
                        [0,-1,-1]])