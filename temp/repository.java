package {{ param.repositoryPackageName }};

import {{ param.dbPackageName }}.{{ param.className }}DB;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import {{ param.modelPackageName }}.{{ param.className }};
import com.nurkiewicz.jdbcrepository.JdbcRepository;
import com.nurkiewicz.jdbcrepository.RowUnmapper;

@Repository("{{ param.classNameHump }}Repository")
public class {{ param.className }}Repository extends JdbcRepository<{{ param.className }}, {{ param.keyType }}> {
    private static Logger LOG = LoggerFactory.getLogger({{ param.className }}Repository.class);
    @Autowired
    private JdbcOperations jdbcOperations;

    protected JdbcOperations getJdbcOperations() {
        return this.jdbcOperations;
    }

    public {{ param.className }}Repository() {
        super({{ param.className }}DB.ROW_MAPPER, {{ param.className }}DB.ROW_UNMAPPER, {{ param.className }}DB.getTableName());
    }

    public {{ param.className }}Repository(RowMapper<{{ param.className }}> rowMapper, RowUnmapper<{{ param.className }}> rowUnmapper,
                                    String idColumn) {
        super(rowMapper, rowUnmapper, {{ param.className }}DB.getTableName(), idColumn);
    }

    @Override
    protected {{ param.className }} postCreate({{ param.className }} entity, Number generatedId) {
        entity.setId(generatedId.longValue());
        entity.setPersisted(true);
        return entity;
    }
}