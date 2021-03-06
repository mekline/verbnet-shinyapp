library(shiny)
library(rPython)
library(rjson)
library(RJSONIO)
library(shinythemes)
library(rsconnect)
library(methods)

python.load("verbnet_search.py")

# Define server logic required to draw a histogram
function(input, output,session) {
   output$selectUI <- renderUI({ 
    selectInput("search2",paste("Select your  ",input$search1),python.call("first_choice",input$search1),selected='')
     })
   
   output$downloadlist1 <- downloadHandler(
    filename = function() { paste(input$search1, '.csv', sep='') },
    content = function(file) {
      write.csv(python.call("first_choice",input$search1), file)})
   
   output$select2 <- renderUI({
     selectInput("search3","Select your verb",python.call("second_choice",input$search1,input$search2),selected='')
   })
   
   output$downloadlist2 <- downloadHandler(
    filename = function() { paste(input$search1, '.csv', sep='') },
    content = function(file) {
      write.csv(python.call("second_choice",input$search1,input$search2), file)})
   
   output$verb <- renderUI({
    python.call("final_print",input$search3) })
   output$url<-renderUI({
     python.call("url",input$search3)
   })
}


