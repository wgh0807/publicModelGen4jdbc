package {{ param.modelPackageName }};

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.springframework.data.domain.Persistable;
{% for item in param.classesNames %}
import {{ item }};{% endfor %}

/**
 * {% if param.classComment %}{{ param.classComment }}{% endif %}
 */
public class {{ param.className }} implements Persistable<{{ param.keyType }}> {
    private static final long serialVersionUID = 1L;
    private transient boolean persisted;
    {% for item in param.properties %}
    /**
     * {{ item.annotation }}
     */
    private {{ item.className }} {{item.name}}{% if item.defaultValue %} = {{ item.defaultValue }} {% endif %};{% endfor %}

    public {{ param.className }}() {
    }

    public boolean isNew() {
        return this.{{ param.keyName }} == null;
    }

    public void setPersisted(Boolean persisted) {
        this.persisted = persisted;
    }

    public Boolean getPersisted() {
        return this.persisted;
    }

    @Override
    public String toString() {
        return ToStringBuilder.reflectionToString(this);
    }

    {% for item in param.properties %}
    public {{ item.className }} get{{ item.humpName }}() {
        return {{ item.name }};
    }

    public void set{{ item.humpName }}({{ item.className }} {{ item.name }}) {
        this.{{ item.name }} = {{ item.name }};
    }
    {% endfor %}
    {% if param.needBuilder  %}public static Builder getBuilder() {
        return new Builder();
    }

    public static class Builder {
        {% for item in param.properties %}/**
        * {{ item.annotation }}
        */
        private {{ item.className }} {{item.name}}{% if item.defaultValue %} = {{ item.defaultValue }} {% endif %};
        {% endfor %}

        {% for item in param.properties %}public Builder {{item.name}}({{ item.className }} {{item.name}}){
            this.{{item.name}} = {{item.name}};
            return this;
        }
        {% endfor %}
        public {{ param.className }} build() {
            return new {{ param.className }}(this);
        }
    }

    private {{ param.className }}(Builder builder) {
        {% for item in param.properties %}this.{{item.name}} = builder.{{item.name}};
        {% endfor %}
    }{% endif %}
}