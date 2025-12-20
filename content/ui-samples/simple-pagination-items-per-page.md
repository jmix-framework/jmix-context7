<Path>Components > SimplePagination > SimplePagination with ItemsPerPage</Path>

SimplePagination can manage the maximum size of the page. This functionality is presented by the following properties: itemsPerPageVisible - defines whether the dropdown list of maximum page size items should be visible. itemsPerPageItems - sets custom maximum page size items that should be used in the dropdown list. Values should be separated by the comma, e.g. "10, 25, 50". itemsPerPageDefaultValue - sets the default value from available items that should be used by default. It can be used even if the itemsPerPageVisible attribute is set to "false". itemsPerPageUnlimitedItemVisible - defines should be item that is shown as empty item in Select visible. If this item is selected the maximum page size will be provided by the entityPageSize application property.

simple-pagination-items-per-page.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer">
            <fetchPlan extends="_local"/>
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
        <simplePagination classNames="self-center"
                          itemsPerPageVisible="true"
                          itemsPerPageItems="5, 10, 15"
                          itemsPerPageDefaultValue="5"
                          dataLoader="customersDl"/>
        <dataGrid id="customersDataGrid"
                  dataContainer="customersDc"
                  width="100%"
                  minHeight="15em">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
            </columns>
        </dataGrid>
    </layout>
</view>




SimplePaginationItemsPerPageSample.java

package io.jmix.uisamples.view.flowui.components.simplepagination.itemsperpage;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("simple-pagination-items-per-page")
@ViewDescriptor("simple-pagination-items-per-page.xml")
public class SimplePaginationItemsPerPageSample extends StandardView {
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


