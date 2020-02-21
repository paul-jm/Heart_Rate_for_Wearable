library(ggplot2)
library ("RCurl")


x11()
data = read.csv("heart_rate.csv")
data <- tail(data,30)
ggplot(data=data, aes(x=time, y=heart_rate, group=1)) +
  geom_line()+
  geom_point()+
  theme(axis.text.x = element_text(angle = 90))
while(T){
Sys.sleep(10)
print("Reading Data")
data = read.csv("heart_rate.csv")
data <- tail(data,30)

print(ggplot(data=data, aes(x=time, y=heart_rate, group=1)) +
  geom_line()+
  geom_point()+
  theme(axis.text.x = element_text(angle = 90)))
}



protocol <- "sftp"
server <- "server_here"
userpwd <- "user_name:password"

tsfrFilename <- "heart_rate.csv"
url <- paste0(protocol, "://", server, tsfrFilename)


data <- getURL(url = url, userpwd=userpwd)
fileConn<-file("output.csv")
writeLines(data, fileConn)
dataframe <- read.csv("output.csv")

x11()

data <- tail(dataframe,75)
ggplot(data=data, aes(x=time, y=heart_rate, group=1)) + 
  geom_line() + 
  theme_light() +
  theme(axis.text.x = element_text(angle=90)) +
  labs(title="Real Time Heart Rate",
       subtitle="InstantHeart",
       y="heart rate", x="time")+
  geom_hline(yintercept=160, linetype="dashed", color = "red") +
  geom_hline(yintercept=40, linetype="dashed", color="red")
while(T){
  Sys.sleep(3)
  print("Reading Data")
  data <- getURL(url = url, userpwd=userpwd)
  fileConn<-file("output.csv")
  writeLines(data, fileConn)
  dataframe <- read.csv("output.csv")
  data <- tail(dataframe,75)
  
  print(ggplot(data=data, aes(x=time, y=heart_rate, group=1)) + 
          geom_line() + 
          theme_light() +
          theme(axis.text.x = element_text(angle=90)) +
          labs(title="Real Time Heart Rate",
               subtitle="InstantHeart",
               y="heart rate", x="time")+
          geom_hline(yintercept=160, linetype="dashed", color = "red") +
          geom_hline(yintercept=40, linetype="dashed", color="red"))
}
