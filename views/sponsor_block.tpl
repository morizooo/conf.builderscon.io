  <div class="section article">
    <div class="inner">
      <h1 class="section-header">{% trans %}Sponsors{% endtrans %}</h1>
      <div class="section-content">
{% for group in conference.sponsors|groupby('group_name') %}
{%   set perrow = 4 %}
{%   if group.grouper == "tier-2" %}
{%     set perrow = 6 %}
{%   endif %} 
{%   set colsize = (12 / perrow)|int %}
        <div class="row sponsor-tier {{ group.grouper }}">
          <div class="large-12 columns">
{% for sponsor in group.list %}
{% if loop.index % perrow == 1 %}<div class="row">{% endif %}
            <div class="large-{{ colsize }} columns">
              <div class="sponsor-slot">
                <a href="{{ sponsor.url }}"><img class="{{ sponsor.group_name }}" src="{{ sponsor.logo_url1 }}"></a>
                <div class="sponsor-name"><a href="{{ sponsor.url }}">{{ sponsor.name }}</a></div>
              </div>
            </div>
{% if loop.index % perrow == 0 or loop.last %}</div><!-- end row -->{% endif %}
{% endfor %}
          </div>
        </div>
{% endfor %}
      </div>
    </div>
  </div>

