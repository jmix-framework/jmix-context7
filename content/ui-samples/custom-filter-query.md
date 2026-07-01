<Path>Cookbook > Data in UI > Custom filter using query modification</Path>

This example shows how to implement a custom filter by programmatically modifying the query text in the TypedValueChangeEvent handler of an input field. See reload() method of CustomFilterQuerySample class. If the filter field is not empty, it adds a where condition to the query text and sets the appropriate query parameter value. The value contains the (?i) prefix which ensures case-insensitive search. The DataLoadCoordinator facet is not used in this example. Instead, the reload() method is invoked on BeforeShowEvent explicitly in the controller. Note also that genericFilter component can be used together with a custom filter.

custom-filter-query.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e order by e.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <layout>
        <genericFilter id="filter" summaryText="Generic filter" opened="false"
                       dataLoader="customersDl">
            <properties include=".*"/>
        </genericFilter>
        <hbox alignItems="END" wrap="true">
            <textField id="nameFilterField" label="Custom filter" placeholder="First or last name" width="15em"/>
            <button id="customersDataGridRefreshBtn" action="customersDataGrid.refresh"/>
        </hbox>
        <dataGrid id="customersDataGrid" dataContainer="customersDc" width="100%">
            <actions>
                <action id="refresh" type="list_refresh"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="email"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>





CustomFilterQuerySample.java

package io.jmix.uisamples.view.flowui.cookbook.customfilterquery;

import com.google.common.base.Strings;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

import java.util.HashMap;
import java.util.Map;

@ViewController("custom-filter-query")
@ViewDescriptor("custom-filter-query.xml")
public class CustomFilterQuerySample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> nameFilterField;
    @ViewComponent
    protected CollectionLoader<Customer> customersDl;

    @Subscribe
    protected void onBeforeShow(BeforeShowEvent event) {
        reload();
    }

    @Subscribe("nameFilterField")
    protected void onNameFilterFieldValueChange(TypedValueChangeEvent<TypedTextField<String>, String> event) {
        reload();
    }

    protected void reload() {
        String query = "select e from Customer e ";
        Map<String, Object> paramsMap = new HashMap<>();

        if (!Strings.isNullOrEmpty(nameFilterField.getTypedValue())) {
            query += "where (e.name like :name or e.lastName like :name)";
            paramsMap.put("name", "(?i)%" + nameFilterField.getTypedValue() + "%");
        }
        query += " order by e.name";

        customersDl.setQuery(query);
        customersDl.setParameters(paramsMap);
        customersDl.load();
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


