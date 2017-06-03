\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{sgreport} [2017/02/25 v0.01 Samuel Gauthier Report LaTeX document class]
\LoadClass[a4paper,twoside]{report}

%%%%%%%%%% For Dev Only
%\RequirePackage[margin=1in,showframe]{geometry}
%\RequirePackage[top=3cm, bottom=3cm, left=3cm, right=2cm, showframe]{geometry}
%%%%%%%%%% For Dev Only

\RequirePackage[top=3cm, bottom=3cm, left=3.5cm, right=3.5cm]{geometry}
%\RequirePackage{graphicx}
\RequirePackage[utf8]{inputenc}
%\RequirePackage{titlesec}
%\RequirePackage[flushmargin,hang]{footmisc}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
%\RequirePackage[Sonny]{fncychap}


%%%%%%%%%% Redefine Header and Footer
\fancyhead{} % lear all fields
\fancyhead[RO,LE]{\textsl{\rightmark}}
\fancyfoot{} % clear all fields
\fancyfoot[RO,LE]{\thepage}
\fancyfoot[LO,RE]{\textsl{\leftmark}}

%%%%%%%%%% Under Work /!\ Redefine Chapter Style
%\titleformat{\chapter}[display]
%    {\flushright\fontfamily{Roboto-LF}\fontseries{t}\fontshape{n}}
%    {\fontsize{96}{96}\selectfont\fontfamily{Roboto-LF}\thechapter}
%    {0pt}
%    {\Huge\rmfamily\fontshape{n}}%\fontfamily{Roboto-LF}\fontseries{t}\fontshape{n}
%\titlespacing{\chapter}{0pt}{0pt}{2\baselineskip}

%%%%%%%%%% Redefine Chapter Layout
%\ChNameVar{\Large\rm} % sets the style for name 
%\ChNumVar{\Huge} % sets the style for digit 
%\ChTitleVar{\Large\rm\centering} % sets the style for title 
%\ChRuleWidth{4pt} % Set RW=4pt
%\ChNameUpperCase % Make name uppercase 
%\renewcommand{\DOCH}{%
%	\setlength{\fboxrule}{\RW} % Let fbox lines be controlled by % \ChRuleWidth
%	\fbox{\CNV\FmN{\@chapapp}\space \CNoV\thechapter}\par\nobreak
%\vskip 40\p@}
%\renewcommand{\DOTI}[1]{% 
%	\CTV\FmTi{#1}\par\nobreak \vskip 40\p@}
%\renewcommand{\DOTIS}[1]{%
%		\CTV\FmTi{#1}\par\nobreak \vskip 40\p@}
%\makeatother

%%%%%%%%%% Define new commands
\newcommand*{\university}[1]{\gdef\@university{#1}%
}
\newcommand*{\@university}{\texttt{\string\university} currently
not set. Please fix this.}

\newcommand*{\project}[1]{\gdef\@project{#1}%
}
\newcommand*{\@project}{\texttt{\string\project} currently
not set. Please fix this.}

\newcommand*{\supervisor}[1]{\gdef\@supervisor{#1}%
}
\newcommand*{\@supervisor}{\texttt{\string\supervisor} currently
not set. Please fix this.}

%%%%%%%%%% Redefine Title Page
\renewcommand*{\maketitle}{%
\begin{titlepage}

\newgeometry{top=3cm, bottom=3cm, left=2cm, right=2cm}
\vspace*{3cm}

\centering
{\scshape\LARGE \@university \par}
\vspace{1cm}

{\scshape\Large\@project\unskip\strut\par}
\vspace{1.5cm}

{
\centering%
\includegraphics[width=4cm]{images/bell-icon.eps}\par
}\vspace{1cm}

{\huge\bfseries\@title\unskip\strut\par}
\vspace{2cm}

{\Large\itshape\@author\unskip\strut\par}
\vspace{4cm}

\vfill
supervised by\par
\@supervisor\unskip\strut\par
\vfill

{\large \@date\par}
\end{titlepage}
}
\endinput




