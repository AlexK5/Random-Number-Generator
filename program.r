library(reticulate)
setwd("/Users/Alexk/Test Project/")
source_python("randomNumber.py")
x <- thing()
scoreTable <- x[[1]]
oprTable <- x[[2]]
