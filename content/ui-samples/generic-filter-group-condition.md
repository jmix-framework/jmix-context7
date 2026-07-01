<Path>Components > GenericFilter > GenericFilter with group condition</Path>

In this example, the configuration was created in design-time in XML, made default using default XML attribute. So it appears right after opening the screen. The filter configuration conditions are contained in the tree. All top-level conditions are joined by logical condition (the default is AND). You can add AND or OR groups to create complex conditions. A user can create group conditions by selecting Create Group condition in the Add search condition dialog. Group conditions can also be defined in the screen XML (groupFilter). You can open the advanced conditions editor by selecting Edit in the settings drop-down menu.

generic-filter-group-condition.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <genericFilter id="genericFilter" dataLoader="customersDl">
            <properties include=".*"/>
            <configurations>
                <configuration id="defaultConfiguration" name="Configuration with conditions grouping" default="true">
                    <groupFilter operation="OR">
                        <propertyFilter property="active" operation="EQUAL"
                                        operationEditable="true" defaultValue="false"/>
                        <propertyFilter property="grade" operation="EQUAL"
                                        operationEditable="true" defaultValue="30"/>
                    </groupFilter>
                    <propertyFilter property="age" operation="GREATER_OR_EQUAL"
                                    operationEditable="true" defaultValue="30"/>
                </configuration>
            </configurations>
        </genericFilter>
        <dataGrid id="customerDataGrid"
                  dataContainer="customersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>




GenericFilterGroupConditionSample.java

package io.jmix.uisamples.view.flowui.components.genericfilter.group;

import io.jmix.core.querycondition.PropertyConditionUtils;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.genericfilter.GenericFilter;
import io.jmix.flowui.component.genericfilter.configuration.DesignTimeConfiguration;
import io.jmix.flowui.component.logicalfilter.GroupFilter;
import io.jmix.flowui.component.logicalfilter.LogicalFilterComponent;
import io.jmix.flowui.component.logicalfilter.LogicalFilterSupport;
import io.jmix.flowui.component.propertyfilter.PropertyFilter;
import io.jmix.flowui.component.propertyfilter.SingleFilterSupport;
import io.jmix.flowui.model.DataLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CustomerGrade;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("generic-filter-group-condition")
@ViewDescriptor("generic-filter-group-condition.xml")
public class GenericFilterGroupConditionSample extends StandardView {

    @ViewComponent
    protected GenericFilter genericFilter;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected SingleFilterSupport singleFilterSupport;
    @Autowired
    protected LogicalFilterSupport logicalFilterSupport;

    @Subscribe
    protected void onInit(InitEvent event) {
        initConfiguration();
    }

    protected void initConfiguration() {
        DesignTimeConfiguration javaConfiguration = genericFilter.addConfiguration("javaConfiguration",
                "Programmatically defined configuration");
        DataLoader dataLoader = genericFilter.getDataLoader();

        GroupFilter groupFilter = createGroupFilter(dataLoader);
        PropertyFilter<Boolean> activePropertyFilter = createActivePropertyFilter(dataLoader);
        PropertyFilter<CustomerGrade> gradePropertyFilter = createGradePropertyFilter(dataLoader);
        groupFilter.add(activePropertyFilter);
        groupFilter.add(gradePropertyFilter);

        PropertyFilter<Integer> agePropertyFilter = createAgePropertyFilter(dataLoader);

        javaConfiguration.getRootLogicalFilterComponent().add(groupFilter);
        javaConfiguration.getRootLogicalFilterComponent().add(agePropertyFilter);

        activePropertyFilter.setValue(false);
        javaConfiguration.setFilterComponentDefaultValue(activePropertyFilter.getParameterName(), false);

        gradePropertyFilter.setValue(CustomerGrade.STANDARD);
        javaConfiguration.setFilterComponentDefaultValue(gradePropertyFilter.getParameterName(), CustomerGrade.STANDARD);

        agePropertyFilter.setValue(30);
        javaConfiguration.setFilterComponentDefaultValue(agePropertyFilter.getParameterName(), 30);
    }

    protected GroupFilter createGroupFilter(DataLoader dataLoader) {
        GroupFilter groupFilter = uiComponents.create(GroupFilter.class);
        groupFilter.setConditionModificationDelegated(true);
        groupFilter.setDataLoader(dataLoader);
        groupFilter.setOperation(LogicalFilterComponent.Operation.OR);

        return groupFilter;
    }

    protected PropertyFilter<Boolean> createActivePropertyFilter(DataLoader dataLoader) {
        PropertyFilter<Boolean> activePropertyFilter = uiComponents.create(PropertyFilter.class);
        activePropertyFilter.setConditionModificationDelegated(true);
        activePropertyFilter.setDataLoader(dataLoader);
        activePropertyFilter.setProperty("active");
        activePropertyFilter.setOperation(PropertyFilter.Operation.EQUAL);
        activePropertyFilter.setOperationEditable(true);

        activePropertyFilter.setParameterName(PropertyConditionUtils.generateParameterName(
                activePropertyFilter.getProperty()));
        activePropertyFilter.setValueComponent(singleFilterSupport.generateValueComponent(
                dataLoader.getContainer().getEntityMetaClass(),
                activePropertyFilter.getProperty(),
                activePropertyFilter.getOperation()
        ));

        return activePropertyFilter;
    }

    protected PropertyFilter<CustomerGrade> createGradePropertyFilter(DataLoader dataLoader) {
        PropertyFilter<CustomerGrade> gradePropertyFilter = uiComponents.create(PropertyFilter.class);
        gradePropertyFilter.setConditionModificationDelegated(true);
        gradePropertyFilter.setDataLoader(dataLoader);
        gradePropertyFilter.setProperty("grade");
        gradePropertyFilter.setOperation(PropertyFilter.Operation.EQUAL);
        gradePropertyFilter.setOperationEditable(true);

        gradePropertyFilter.setParameterName(PropertyConditionUtils.generateParameterName(
                gradePropertyFilter.getProperty()));
        gradePropertyFilter.setValueComponent(singleFilterSupport.generateValueComponent(
                dataLoader.getContainer().getEntityMetaClass(),
                gradePropertyFilter.getProperty(),
                gradePropertyFilter.getOperation()
        ));

        return gradePropertyFilter;
    }

    protected PropertyFilter<Integer> createAgePropertyFilter(DataLoader dataLoader) {
        PropertyFilter<Integer> agePropertyFilter = uiComponents.create(PropertyFilter.class);
        agePropertyFilter.setConditionModificationDelegated(true);
        agePropertyFilter.setDataLoader(dataLoader);
        agePropertyFilter.setProperty("age");
        agePropertyFilter.setOperation(PropertyFilter.Operation.GREATER_OR_EQUAL);
        agePropertyFilter.setOperationEditable(true);

        agePropertyFilter.setParameterName(PropertyConditionUtils.generateParameterName(
                agePropertyFilter.getProperty()));
        agePropertyFilter.setValueComponent(singleFilterSupport.generateValueComponent(
                dataLoader.getContainer().getEntityMetaClass(),
                agePropertyFilter.getProperty(),
                agePropertyFilter.getOperation()
        ));

        return agePropertyFilter;
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}


