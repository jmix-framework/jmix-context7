<Path>Components > DataGrid > DataGrid with aggregation</Path>

aggregatable attribute enables aggregation for DataGrid rows. The following operations are supported: SUM - calculate the sum AVG - find the average value COUNT - calculate the total number MIN - find the minimum value MAX - find the maximum value The aggregation element should be set for aggregated DataGrid cells with the type attribute, which sets the aggregation function. The aggregated table values are shown in an additional row at the bottom of the DataGrid. The aggregationPosition attribute allows you to specify the location of the aggregation row: TOP or BOTTOM. BOTTOM is used by default. In addition to the operations listed above, you can define a custom aggregation strategy by implementing the AggregationStrategy interface.

data-grid-aggregation.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="ordersLoader">
                <query>
                    <![CDATA[select e from uisamples_Order e order by e.date]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <dataGrid id="ordersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="ordersDc"
                  aggregatable="true"
                  aggregationPosition="TOP">
            <columns>
                <column property="date"/>
                <column property="customer"/>
                <column property="customer.grade">
                    <aggregation
                            strategyClass="io.jmix.uisamples.view.flowui.components.datagrid.aggregation.DataGridCustomerGradeAggregation"/>
                </column>
                <column property="amount">
                    <aggregation type="SUM"/>
                </column>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridAggregationSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.aggregation;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("data-grid-aggregation")
@ViewDescriptor("data-grid-aggregation.xml")
public class DataGridAggregationSample extends StandardView {
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




Order.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Table(name = "ORDER")
@Entity(name = "uisamples_Order")
@JmixEntity
public class Order {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "CUSTOMER_ID")
    private Customer customer;

    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_", nullable = false)
    @InstanceName
    private Date date;

    @Column(name = "AMOUNT")
    private BigDecimal amount;

    @Column(name = "DESCRIPTION")
    private String description;

    @OrderBy("rowNum")
    @Composition
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Date getDate() {
        return date;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
    }
}




DataGridCustomerGradeAggregation.java

package io.jmix.uisamples.view.flowui.components.datagrid.aggregation;

import io.jmix.core.Messages;
import io.jmix.flowui.data.aggregation.AggregationStrategy;
import io.jmix.uisamples.entity.CustomerGrade;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;

/**
 * Calculates the most frequent customer grade
 */
public class DataGridCustomerGradeAggregation implements AggregationStrategy<CustomerGrade, String> {

    @Autowired
    public Messages messages;

    @Override
    public String aggregate(Collection<CustomerGrade> propertyValues) {
        CustomerGrade mostFrequent = null;
        long max = 0;

        if (CollectionUtils.isNotEmpty(propertyValues)) {
            for (CustomerGrade grade : CustomerGrade.values()) {
                long current = propertyValues.stream()
                        .filter(grade::equals)
                        .count();

                if (current > max) {
                    mostFrequent = grade;
                    max = current;
                }
            }
        }

        if (mostFrequent != null) {
            String key = CustomerGrade.class.getSimpleName() + "." + mostFrequent.name();
            return String.format("%s: %d/%d", messages.getMessage(CustomerGrade.class, key), max, propertyValues.size());
        }

        return "NaN";
    }

    @Override
    public Class<String> getResultClass() {
        return String.class;
    }
}


