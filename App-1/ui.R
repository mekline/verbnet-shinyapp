library(shiny)
library(rPython)
setwd("/Users/laurenskorb/Documents/L3_Lab_Admin_Docs/verbnet/")
python.load("/Users/laurenskorb/Documents/L3_Lab_Admin_Docs/verbnet/verbnet_search.py")
all_classes <- python.get("class_list")
all_classes<-as.list(all_classes)
all_verbs <- python.get("all_verbs")
all_verbs<-as.list(all_verbs)
# Define UI for application that draws a histogram
fluidPage(
  titlePanel("Exploring Verbnet"),
  fluidRow(selectInput('class', label = h3("Select verb class to see all verbs"),choices = as.character(all_classes))),
  fluidRow(verbatimTextOutput("out1")),
  fluidRow(selectInput('verb', label = h3("Select verb to see all possible frames"),choices = as.character(all_verbs))),
  fluidRow(verbatimTextOutput("out2")),
  fluidRow(selectInput('verb1', label = h3("Select verb to see if it takes an agent."),choices = as.character(all_verbs))),
  fluidRow(verbatimTextOutput("out3")),
  fluidRow(selectInput('verb2', label = h3("Select verb to see if it takes a patient."),choices = as.character(all_verbs))),
  fluidRow(verbatimTextOutput("out4"))
  )
  
