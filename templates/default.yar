{% if ruleTag %}rule {{ ruleName }} : {{ ruleTag }} { {% else %}rule {{ ruleName }} { {%endif %}
meta:
  author = "{{ authorName }}"
  date = "{{ date }}"
  description = "{{ desc }}"
  {% for hash in hashArray -%}
  hash{{ loop.index }} = "{{ hash }}"
  {% endfor -%}
  sample_filetype = "{{ fileType }}"
  yarasilly2 = "https://github.com/YARA-Silly-Silly/yarasilly2"
strings:
  {%- for pattern in patterns %}
  $string{{loop.index}} = {{ pattern }}{% endfor %}
condition:
  {{ condition }}
}
