<Path>Facets > Settings</Path>

Settings facet is designed to persist the state of UI components or custom data in a database in FLOWUI_USER_SETTINGS table. UserSettingsItem JPA entity is used for saving state. To enable settings in a View, it should contain the SettingsFacet. The simplest way to add facet is XML. Facet with auto="true" tries to find all components with defined ID that supports settings. All these components will save and apply their settings. Supported components: DataGrid: saves order, sorting and visibility of columns Details: saves opened state SimplePagination: saves maxResults, if itemsPerPageVisible attribute is true GenericFilter: saves opened state This sample uses DataGrid and Details components to demonstrate how settings facet works. The initial state of the Details component is set to opened. You can change this state, then go to another view and return. The last state will be restored. The same is possible for a DataGrid component.

settings-facet.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
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
        <settings auto="true"/>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <details id="details" summaryText="DataGrid details" opened="true" width="100%">
            <dataGrid id="customersDataGrid"
                      width="100%"
                      minHeight="20em"
                      columnReorderingAllowed="true"
                      dataContainer="customersDc">
                <columns>
                    <column property="name"/>
                    <column property="lastName"/>
                    <column property="email"/>
                    <column property="age"/>
                    <column property="active"/>
                    <column property="grade"/>
                </columns>
            </dataGrid>
        </details>
    </layout>
</view>




SettingsFacetSample.java

package io.jmix.uisamples.view.flowui.facets.settings;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("settings-facet")
@ViewDescriptor("settings-facet.xml")
public class SettingsFacetSample extends StandardView {
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


