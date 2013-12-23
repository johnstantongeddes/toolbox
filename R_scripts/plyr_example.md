qPCR analysis
========================================================

Preliminary analysis of Andrew's qPCR data.


```r
library(plyr)
```



```r
data <- read.csv("plyr_example_data.csv", skip = 3, as.is = TRUE)
head(data)
```

```
##   Well target dilution           C_
## 1   A1    18s    1e+00 Undetermined
## 2   A2    18s    1e-01 Undetermined
## 3   A3    18s    1e-02 Undetermined
## 4   A4    18s    1e-03 Undetermined
## 5   A5    18s    1e-04 Undetermined
## 6   A6    18s    0e+00  35.70304489
```

```r
str(data)
```

```
## 'data.frame':	96 obs. of  4 variables:
##  $ Well    : chr  "A1" "A2" "A3" "A4" ...
##  $ target  : chr  "18s" "18s" "18s" "18s" ...
##  $ dilution: num  1e+00 1e-01 1e-02 1e-03 1e-04 0e+00 1e+00 1e-01 1e-02 1e-03 ...
##  $ C_      : chr  "Undetermined" "Undetermined" "Undetermined" "Undetermined" ...
```


Modifications to data file. 

* Rename `C_` to `Ct` 
* Assign `Ct` "Undetermined" to NA
* Convert `Ct` to numeric
* Convert `target` to factor


```r
colnames(data)[4] <- "Ct"
data[data$Ct == "Undetermined", "Ct"] <- NA
data$Ct <- as.numeric(data$Ct)
data$target <- as.factor(data$target)
head(data)
```

```
##   Well target dilution   Ct
## 1   A1    18s    1e+00   NA
## 2   A2    18s    1e-01   NA
## 3   A3    18s    1e-02   NA
## 4   A4    18s    1e-03   NA
## 5   A5    18s    1e-04   NA
## 6   A6    18s    0e+00 35.7
```

```r
str(data)
```

```
## 'data.frame':	96 obs. of  4 variables:
##  $ Well    : chr  "A1" "A2" "A3" "A4" ...
##  $ target  : Factor w/ 8 levels "18s","ef1b","gapdh",..: 1 1 1 1 1 1 6 6 6 6 ...
##  $ dilution: num  1e+00 1e-01 1e-02 1e-03 1e-04 0e+00 1e+00 1e-01 1e-02 1e-03 ...
##  $ Ct      : num  NA NA NA NA NA ...
```

```r
summary(data)
```

```
##      Well                  target      dilution            Ct       
##  Length:96          18s       :12   Min.   :0.0000   Min.   : 6.09  
##  Class :character   ef1b      :12   1st Qu.:0.0001   1st Qu.: 7.97  
##  Mode  :character   gapdh     :12   Median :0.0055   Median :24.54  
##                     H3        :12   Mean   :0.1852   Mean   :21.59  
##                     hsc70-4 h1:12   3rd Qu.:0.1000   3rd Qu.:32.53  
##                     hsc70-4 h2:12   Max.   :1.0000   Max.   :39.51  
##                     (Other)   :24                    NA's   :24
```

```r
levels(data$target)
```

```
## [1] "18s"        "ef1b"       "gapdh"      "H3"         "hsc70-4 h1"
## [6] "hsc70-4 h2" "hsp83"      "rps20"
```


Generate a histogram of *Ct*


```r
hist(data$Ct)
```

![plot of chunk hist](figure/hist.png) 




```r
datasub <- subset(data, dilution != 0, )
datasub <- na.exclude(datasub)
str(datasub)
```

```
## 'data.frame':	69 obs. of  4 variables:
##  $ Well    : chr  "A7" "A8" "A9" "A10" ...
##  $ target  : Factor w/ 8 levels "18s","ef1b","gapdh",..: 6 6 6 6 6 6 6 6 6 6 ...
##  $ dilution: num  1e+00 1e-01 1e-02 1e-03 1e-04 1e+00 1e-01 1e-02 1e-03 1e-04 ...
##  $ Ct      : num  6.68 20.37 23.8 27.49 30.77 ...
##  - attr(*, "na.action")=Class 'exclude'  Named int [1:11] 1 2 3 4 5 11 12 13 14 15 ...
##   .. ..- attr(*, "names")= chr [1:11] "1" "2" "3" "4" ...
```

```r

# ddply(datasub, .(target, dilution), summarize, mean = mean(Ct,
# na.rm=TRUE)) ddply(datasub, .(target), summarize, table(dilution))
# ddply(datasub, .(target, dilution), summarize, table(Ct))

ddply(datasub, .(target), summarize, slope = lm(Ct ~ log(dilution))$coef[2])
```

```
##       target    slope
## 1       ef1b -2.53769
## 2      gapdh -2.41734
## 3         H3 -0.07628
## 4 hsc70-4 h1 -0.11002
## 5 hsc70-4 h2 -2.33714
## 6      hsp83 -0.09739
## 7      rps20 -2.93323
```


