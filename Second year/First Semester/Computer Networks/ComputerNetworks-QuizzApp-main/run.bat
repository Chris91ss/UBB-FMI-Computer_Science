if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
java --module-path ".\Files\javafx-sdk-17.0.1\lib" --add-modules javafx.controls,javafx.fxml -jar .\Files\Quizz.jar
exit