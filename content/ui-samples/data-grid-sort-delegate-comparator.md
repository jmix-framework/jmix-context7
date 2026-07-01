<Path>Components > DataGrid > DataGrid sort delegate by comparator</Path>

`DataGrid.setSortBuilderDelegate()` customizes how a column is sorted.

The sample above sorts the *Grade* column by a custom business priority (HIGH, then PREMIUM, then STANDARD) instead of the default enumeration order, using a `Comparator` supplied through `DataGridSortBuilder.replaceSort()`.

Without the delegate, the column sorts by the declaration order of its constants (PREMIUM, HIGH, STANDARD), because Java enums are `Comparable` by `ordinal()`.

Comparators are applied for in-memory sorting, which happens here because the whole dataset is loaded on the client. For database (persistent) sorting, supply a JPQL expression instead.


data-grid-sort-delegate-comparator.xml

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
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridSortDelegateComparatorSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.sortdelegatecomparator;

import io.jmix.flowui.component.grid.DataGridSortContext;
import io.jmix.flowui.component.grid.sort.DataGridSort;
import io.jmix.flowui.component.grid.sort.DataGridSortBuilder;
import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;

import java.util.Comparator;
import java.util.List;

@ViewController("data-grid-sort-delegate-comparator")
@ViewDescriptor("data-grid-sort-delegate-comparator.xml")
public class DataGridSortDelegateComparatorSample extends StandardView {

    private static final List<CustomerGrade> GRADE_PRIORITY =
            List.of(CustomerGrade.HIGH, CustomerGrade.PREMIUM, CustomerGrade.STANDARD);

    @Install(to = "customersDataGrid", subject = "sortBuilderDelegate")
    public DataGridSort customersDataGridSortBuilderDelegate(DataGridSortContext<Customer> context) {
        return DataGridSortBuilder.create(context)
                .replaceSort("grade", gradePriorityComparator())
                .build();
    }

    private Comparator<Customer> gradePriorityComparator() {
        return Comparator.comparing(Customer::getGrade,
                        Comparator.nullsLast(Comparator.comparingInt(GRADE_PRIORITY::indexOf)))
                .thenComparing(Customer::getName)
                .thenComparing(Customer::getLastName);
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




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


