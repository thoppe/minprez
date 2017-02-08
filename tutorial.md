---- .aligncenter .bg-white
@background(url="https://source.unsplash.com/4mta-DkJUAg") .dark
.text-data  @h3 **miniprez** 
@h4 Beautiful presentations in minimalist format <br>

@p .text-intro 
  miniprez is a static, mobile-friendly version of [webslides](https://github.com/jlantunez/webslides)

@footer
 .wrap
  .span
   .alignleft
     @button(href="https://github.com/thoppe/miniprez") .ghost ::github:: Project repo
   .alignright
     @button(href="https://twitter.com/metasemantic") .ghost ::twitter:: @metasemantic

---- .align-left .bg-black
@background(url="https://source.unsplash.com/aJTiW00qqtI/") .dark

.text-landing .text-content _Slide 2_
@h2 _simple markdown support_
Basic [Markdown](https://daringfireball.net/projects/markdown/syntax) support
@line
 .grid .wrap
  .column
    @h2 :fire: **bold**
    @p `**text**`
  .column
    @h2 :cloud: _emph_
    @p `_text_`
  .column
    @h2 :computer: `code`
    @p `&&&`code&&&`` 

---- .align-left
.text-landing Slide 3
@h2 _emoji_
Standard emoji and [font-awesome](http://fontawesome.io/)  
@line

 .grid .wrap
  .column `:battery:`
    @h1 :battery:
  .column `:heart_eyes:`
    @h1 :heart_eyes:
  .column `::meetup::`
    @h1 ::meetup::
  .column `::ra::`
    @h1 ::ra:: 

---- .bg-apple .align-left
.text-landing Slide 4
@h2 _math support_
LaTeX rendered inline with [KaTex](https://github.com/Khan/KaTeX)  
@line
@h3
  $$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$
<br>
`$$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$`

---- .align-left 
.text-landing Slide 5
@h2 _pretty code blocks_
Syntax highlighting Google's [code prettify](https://github.com/google/code-prettify)  
@line
```
sort [] = []
sort (x:xs) = sort lower ++ [x] ++ sort higher
    where
        lower = filter (< x) xs
        higher = filter (>= x) xs
```
Code blocks are context-aware
```
// to convert prefix to postfix
main() {
  char c = getchar();
  (c == '+' || c == '-' || c == '*' || c == '/') ? main(), main() : 0;
  putchar(c);
} 
```

-----
@video(autoplay="" loop="") .background-video 
  @source(src="https://cdn.shutterstock.com/shutterstock/videos/15778135/preview/stock-footage-office-chair-race-slow-motion-young-guys-have-fun-in-the-office-during-a-break-games-of-businessm.mp4")

.wrap
 .text-landing Slide 6
 @h2 _looping background animations_
 Embed any video file (thanks [Shutterstock](https://www.shutterstock.com/)!)


----- .bg-white .aligncenter
@background(url="https://source.unsplash.com/IEe2c3kyERo") 

  .grid 
   .column .bg-white
    ```
- - - -
@background(url="https://source.unsplash.com/IEe2c3kyERo") 
@h1 It's easy to make a slide with :heart_eyes:
A slide that is **bold** and _exciting_ with
@p $$i \hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat H \Psi(\mathbf{r},t)$$
    ```
   .column
   .column .bg-white
    @h1 It's easy to make a slide with :heart_eyes:
    A slide that is **bold** and _exciting_ with
    @p $$i \hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat H \Psi(\mathbf{r},t)$$

----- .bg-apple

@h1 .text-data Thanks, you!

@footer
  @h4 Contribute at
  @h2 [https://github.com/thoppe/miniprez](https://github.com/thoppe/miniprez)