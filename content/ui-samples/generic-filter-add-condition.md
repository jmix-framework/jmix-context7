<Path>Components > GenericFilter > Add condition to existing configuration</Path>

In this example, a programmatically created filter component has been added to current configuration.

generic-filter-add-condition.xml

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




GenericFilterAddConditionSample.java

package io.jmix.uisamples.view.flowui.components.genericfilter.add;

import io.jmix.core.querycondition.PropertyConditionUtils;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.genericfilter.GenericFilter;
import io.jmix.flowui.component.propertyfilter.PropertyFilter;
import io.jmix.flowui.component.propertyfilter.SingleFilterSupport;
import io.jmix.flowui.model.DataLoader;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("generic-filter-add-condition")
@ViewDescriptor("generic-filter-add-condition.xml")
public class GenericFilterAddConditionSample extends StandardView {

    @ViewComponent
    protected GenericFilter genericFilter;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected SingleFilterSupport singleFilterSupport;

    @Subscribe
    protected void onBeforeShow(BeforeShowEvent event) {
        initConfiguration();
    }

    protected void initConfiguration() {
        DataLoader dataLoader = genericFilter.getDataLoader();
        PropertyFilter<Integer> agePropertyFilter = craeteAgePropertyFilter(dataLoader);

        genericFilter.getCurrentConfiguration().getRootLogicalFilterComponent().add(agePropertyFilter);
        genericFilter.setCurrentConfiguration(genericFilter.getCurrentConfiguration());
    }

    protected PropertyFilter<Integer> craeteAgePropertyFilter(DataLoader dataLoader) {
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
import org.springframework.lang.Nullable;

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


