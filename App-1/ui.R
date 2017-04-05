library(shiny)
library(rPython)
setwd("/Users/laurenskorb/Repos/shiny_verbnet/verbnet/")
python.load("/Users/laurenskorb/Repos/shiny_verbnet/verbnet/verbnet_search.py")
search_list<-c("verb","class","role","frame")

# Define UI for application that draws a histogram

shinyUI(fluidPage(
  titlePanel("Exploring Verbnet"),
  fluidRow(selectInput('search1', label = h3("Search on:"),choices = as.character(search_list))),
  fluidRow(htmlOutput('selectUI')),
  downloadButton('downloadlist1', 'Download'),
  fluidRow(htmlOutput('select2')),
  downloadButton('downloadlist2', 'Download'),
  fluidRow(htmlOutput("verb",container = pre))
  ))
