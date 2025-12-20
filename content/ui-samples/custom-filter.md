<Path>Cookbook > Data in UI > Custom filter using declarative conditions</Path>

This example shows how to implement a custom filter by declaring a set of query conditions linked with an input field by DataLoadCoordinator. DataLoadCoordinator in the automatic mode is also responsible for triggering data loaders on BeforeShowEvent. Note also that genericFilter component can be used together with a custom filter.

custom-filter.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:c="http://jmix.io/schema/flowui/jpql-condition">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e order by e.name]]>
                    <condition>
                        <and>
                            <or>
                                <c:jpql>
                                    <c:where>e.name like :component_nameFilterField</c:where>
                                </c:jpql>
                                <c:jpql>
                                    <c:where>e.lastName like :component_nameFilterField</c:where>
                                </c:jpql>
                            </or>
                        </and>
                    </condition>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <genericFilter id="filter" summaryText="Generic filter" opened="false"
                dataLoader="customersDl">
            <properties include=".*"/>
        </genericFilter>
        <hbox alignItems="END" classNames="flex-wrap">
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
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>





CustomFilterSample.java

package io.jmix.uisamples.view.flowui.cookbook.customfilter;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("custom-filter")
@ViewDescriptor("custom-filter.xml")
public class CustomFilterSample extends StandardView {
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


