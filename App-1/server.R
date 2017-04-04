library(shiny)
library(rPython)
library(rjson)
setwd("/Users/laurenskorb/Documents/L3_Lab_Admin_Docs/verbnet/")
python.load("/Users/laurenskorb/Documents/L3_Lab_Admin_Docs/verbnet/verbnet_search.py")

# Define server logic required to draw a histogram
function(input, output, session) {
  
  # You can access the value of the widget with input$select, e.g.
  output$out1 <- renderPrint({ 
    python.call("class_to_verbs",input$class) })
  output$out2<- renderPrint({
    python.call("frames_given_verb",input$verb)})
  output$out3<- renderPrint({
    python.call("agent_given_verb",input$verb1,'Agent')})
  output$out4<- renderPrint({
    python.call("agent_given_verb",input$verb2,'Patient')})
}

