<h1 align="center">
  <br>
  Automating My Enlightenment
  <br>
</h1>

<h2 align="center">
  <br>
  Real Estate Property Analysis
  <br>
</h2>

Simple Real Estate Return Analysis **Open-source Web Application**. Easy to use, developed as a side project to quickly analyze and compare Residential Properties. 


![Watch the video](/markdown/property_analysis_demo_intro.gif)


## Prerequisite

In order to run it locally, it is required to have python installed in your computer. In addition to that, several specific packages will be required  [_(see requiremts.txt)_](https://github.com/crankstorn/real-estate-analysis/blob/main/requirements.txt)


## Convert to PDF

So far, Streamlit package has not added any convert to PDF functionality. However, we can quickly generate a PDF from the same web browser using the Ctrl + P (for Windows) or Command + P (for macOS) and selecting the option save as a PDF.

Example of the printed PDF image:

![Good PDF print](/markdown/property_analysis_demo.PNG)




Remember to press the `X` button on the Sidebar Segment, otherwise you will end up with a print like this one:

![Bad PDF print](/markdown/property_analysis_demo_fail.PNG)


## Executing locally

1. Fork this repository, by clicking the `Fork` button at the top-right on this page.
[Learn how to fork GitHub projects](https://guides.github.com/activities/forking/)

2. Clone the forked repository from your GitHub account.
```
git clone https://github.com/[replace-with-your-github-username]/real-estate-analysis.git
```

3. From your prompt or terminal, using the path where you saved the script, run it with streamlit with the following comand:
```
streamlit run [full path to saved file]
```

## Non Parametric program assumptions

Currently, the Real Estate Return Analysis web application is generating it's results tanking into account the following assumptions:
* Property insurance value will be represented as a 1% value of the monthly rent.
* CapEx + Repairs value will be represented as a 2% of the overall property value, subsequently being charged on a monthly basis.
* Vacancy value will be represented as a 2% value of the monthly rent.

In future versions, those values will be added into the "Optional inputs" section.

In addition, the Loan Amortization Schedule Plot and Displayable Table are following the French Amortization System. 

## Credits

This project uses several open source packages:

- [pandas](https://pandas.pydata.org/)
- [streamlit](https://www.streamlit.io/)
- [numpy](https://numpy.org/)

This project has been inspired mainly by the following posts:
- [Build a loan amortization schedule with Python](https://www.christopheryee.org/blog/build-a-loan-amortization-schedule-with-python/)
- [Understanding the Mortgage Payment Structure](https://www.investopedia.com/mortgage/mortgage-rates/payment-structure/)
- [Automating Real Estate Investment Analysis: Python Web Scraping Bot](https://towardsdatascience.com/automating-real-estate-investment-analysis-d2b07395833b)
- [Calculating Principal And Interest Payments For A Loan Using Python And Numpy](https://pythontic.com/finance/numpy/ppmt%20and%20ipmt)
- [The Ultimate Personal Web Resume](https://github.com/guilhermeborgesbastos/live-resume)

---

> LinkedIn [profile](https://www.linkedin.com/in/carlos-ramirez-hernandez/)<br>
