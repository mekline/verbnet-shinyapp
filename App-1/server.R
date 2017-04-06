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
    selectInput("search2","Select your choice",python.call("first_choice",input$search1))
     })
   
   output$downloadlist1 <- downloadHandler(
    filename = function() { paste(input$search1, '.csv', sep='') },
    content = function(file) {
      write.csv(python.call("first_choice",input$search1), file)})
   
   output$select2 <- renderUI({
     selectInput("search3","Select your verb",python.call("return_verb_list",input$search2,input$search1))
   })
   
   output$downloadlist2 <- downloadHandler(
    filename = function() { paste(input$search1, '.csv', sep='') },
    content = function(file) {
      write.csv(python.call("second_choice",input$search1,input$search2), file)})
   
   output$verb <- renderUI({
    python.call("final_print",input$search3) })
}


