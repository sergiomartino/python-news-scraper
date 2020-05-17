<ol>
% for article in attrs["articles"]:
    <li>
      <h4>${article.title}</h4>
      <p><em>${article.subtitle}</em></p>
    </li>
% endfor
</ol>