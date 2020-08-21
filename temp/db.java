package {{ param.dbPackageName }};

import {{ param.modelPackageName }}.{{ param.className }};
import com.nurkiewicz.jdbcrepository.RowUnmapper;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

public class {{ param.className }}DB
{

	private static String TABLE_NAME = "{{ param.table_name }}";

	private static String TABLE_ALIAS = "{{ param.tableAlias }}";

	public static String getTableName() {
		return TABLE_NAME;
	}

	public static String getTableAlias() {
		return TABLE_NAME + " as " + TABLE_ALIAS;
	}

	public static String getAlias() {
		return TABLE_ALIAS;
	}

	public static String selectAllColumns(boolean ... useAlias) {
		return (useAlias[0] ? TABLE_ALIAS : TABLE_NAME) + ".*";
	}

	public enum COLUMNS {
	    {% for item in param.properties %}
	    {{ item.upperColumn }}("{{ item.column }}"),{% endfor %}
		;

		private String columnName;

		private COLUMNS (String columnName) {
			this.columnName = columnName;
		}

		public void setColumnName (String columnName) {
			this.columnName = columnName;
		}

		public String getColumnName () {
			return this.columnName;
		}

		public String getColumnAlias () {
			return TABLE_ALIAS + "." + this.columnName;
		}

		public String getColumnAliasAsName () {
			return TABLE_ALIAS  + "." + this.columnName + " as " + TABLE_ALIAS + "_" + this.columnName;
		}

		public String getColumnAliasName () {
			return TABLE_ALIAS + "_" + this.columnName;
		}

	}

	public {{ param.className }}DB () {

	}

	public static final RowMapper<{{ param.className }}> ROW_MAPPER = new RowMapper<{{ param.className }}>() {
		public {{ param.className }} mapRow(ResultSet rs, int rowNum) throws SQLException {
			{{ param.className }} obj = new {{ param.className }}();
			String s = null;
			{% for item in param.properties %}
			{% if item.valueMethod == 'getInt' %} s = rs.getString(COLUMNS.{{ item.upperColumn }}.getColumnName());
			if (Objects.nonNull(s) && s.length()>0) {
				obj.set{{ item.humpName }}(Integer.valueOf(s));
			}{% elif item.valueMethod == 'getLong' %}s = rs.getString(COLUMNS.{{ item.upperColumn }}.getColumnName());
			if (Objects.nonNull(s) && s.length()>0) {
				obj.set{{ item.humpName }}(Long.valueOf(s));
			}{% else %}obj.set{{ item.humpName }}(rs.{{ item.valueMethod }}(COLUMNS.{{ item.upperColumn }}.getColumnName()));{% endif %}{% endfor %}
			return obj;
		}
	};

	public static final RowUnmapper<{{ param.className }}> ROW_UNMAPPER = new RowUnmapper<{{ param.className }}>() {
		public Map<String, Object> mapColumns({{ param.className }} obj) {
			Map<String, Object> mapping = new LinkedHashMap<String, Object>();
			{% for item in param.properties %}
            {% if item.valueMethod == 'getTimestamp' %}if (obj.get{{ item.humpName }}() != null)mapping.put(COLUMNS.{{ item.upperColumn }}.getColumnName(), new Timestamp (obj.get{{ item.humpName }}().getTime()));{% else %}mapping.put(COLUMNS.{{ item.upperColumn }}.getColumnName(), obj.get{{ item.humpName }}());{% endif %}{% endfor %}
			return mapping;
		}
	};

	public static final RowMapper<{{ param.className }}> ALIAS_ROW_MAPPER = new RowMapper<{{ param.className }}>() {
		public {{ param.className }} mapRow(ResultSet rs, int rowNum) throws SQLException {
			{{ param.className }} obj = new {{ param.className }}();
			String s = null;

			{% for item in param.properties %}
			{% if item.valueMethod == 'getInt' %} s = rs.getString(COLUMNS.{{ item.upperColumn }}.getColumnAliasName());
			if (Objects.nonNull(s) && s.length()>0) {
				obj.set{{ item.humpName }}(Integer.valueOf(s));
			}{% elif item.valueMethod == 'getLong' %}s = rs.getString(COLUMNS.{{ item.upperColumn }}.getColumnAliasName());
			if (Objects.nonNull(s) && s.length()>0) {
				obj.set{{ item.humpName }}(Long.valueOf(s));
			}{% else %}obj.set{{ item.humpName }}(rs.{{ item.valueMethod }}(COLUMNS.{{ item.upperColumn }}.getColumnAliasName()));{% endif %}{% endfor %}
			return obj;
		}
	};

	public static StringBuffer getAllColumnAliases () {
		StringBuffer strBuf = new StringBuffer ();
		int i = COLUMNS.values ().length;
		for (COLUMNS c : COLUMNS.values ()) {
			strBuf.append (c.getColumnAliasAsName ());
			if (--i > 0)
				strBuf.append (", ");
		}
		return strBuf;
	}
}