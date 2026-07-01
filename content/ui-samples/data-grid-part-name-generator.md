<Path>Components > DataGrid > DataGrid with part name generator</Path>

You can customize the style of the column by using the @Install annotation. Set the value of the to parameter according to the pattern: {data-grid-id}.{column-name}. In this example, the id is customersDataGrid and the column name is grade. For the subject parameter, assign the partNameGenerator as its value. The method should receive the entity connected to the corresponding data container as an argument. In our case, it is Customer. Finally, implement the required logic within the method body. The corresponding styles for the return values are described in the .css file.

data-grid-part-name-generator.xml

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
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
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
    </layout>
</view>




DataGridPartNameGeneratorSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.partnamegenerator;

import io.jmix.core.Metadata;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-part-name-generator")
@ViewDescriptor("data-grid-part-name-generator.xml")
public class DataGridPartNameGeneratorSample extends StandardView {

    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected Metadata metadata;

    @Install(to = "customersDataGrid.grade", subject = "partNameGenerator")
    protected String gradePartNameGenerator(final Customer customer) {
        if (customer.getGrade() == null) {
            return null;
        }
        return switch (customer.getGrade()) {
            case STANDARD -> "standard-grade";
            case HIGH -> "high-grade";
            case PREMIUM -> "premium-grade";
        };
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




data-grid-part-name-generator.css


vaadin-grid::part(high-grade) {
    background-color: color-mix(in srgb, var(--aura-green) 10%, transparent);
}

vaadin-grid::part(standard-grade) {
    background-color: var(--vaadin-background-container-strong);
}

vaadin-grid::part(premium-grade) {
    background-color: color-mix(in srgb, var(--aura-accent-color) 10%, transparent);
}

vaadin-grid::part(font-weight-bold) {
    font-weight: bold;
}


