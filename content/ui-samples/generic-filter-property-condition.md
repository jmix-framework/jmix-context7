<Path>Components > GenericFilter > GenericFilter with property condition</Path>

In this example, the configuration was created in design-time in XML, made default using default XML attribute. So it appears right after opening the screen. You can easily filter by related entities and their attributes by: selecting entity attribute from Properties group of Add search condition dialog. selecting Create Property condition in the Add search condition dialog. defining condition in the screen XML (propertyFilter). In this example, the list of orders is filtered by customers and by customer grades.

generic-filter-property-condition.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="ordersDl">
                <query>
                    <![CDATA[select e from uisamples_Order e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <genericFilter id="genericFilter" dataLoader="ordersDl">
            <properties include=".*"/>
            <configurations>
                <configuration id="defaultConfiguration" name="Configuration with property conditions" default="true">
                    <propertyFilter property="customer" operation="EQUAL"
                                    operationEditable="true"/>
                    <propertyFilter property="customer.grade" operation="EQUAL"
                                    operationEditable="true"/>
                </configuration>
            </configurations>
        </genericFilter>
        <dataGrid id="ordersDataGrid"
                  dataContainer="ordersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="customer"/>
                <column property="date"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




GenericFilterPropertyConditionSample.java

package io.jmix.uisamples.view.flowui.components.genericfilter.property;

import io.jmix.core.querycondition.PropertyConditionUtils;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.genericfilter.GenericFilter;
import io.jmix.flowui.component.genericfilter.configuration.DesignTimeConfiguration;
import io.jmix.flowui.component.propertyfilter.PropertyFilter;
import io.jmix.flowui.component.propertyfilter.SingleFilterSupport;
import io.jmix.flowui.model.DataLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("generic-filter-property-condition")
@ViewDescriptor("generic-filter-property-condition.xml")
public class GenericFilterPropertyConditionSample extends StandardView {

    @ViewComponent
    protected GenericFilter genericFilter;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected SingleFilterSupport singleFilterSupport;

    @Subscribe
    protected void onInit(InitEvent event) {
        initConfiguration();
    }

    protected void initConfiguration() {
        DesignTimeConfiguration javaConfiguration = genericFilter.addConfiguration("javaConfiguration",
                "Programmatically defined configuration");
        DataLoader dataLoader = genericFilter.getDataLoader();

        javaConfiguration.getRootLogicalFilterComponent().add(createCustomerPropertyFilter(dataLoader));
        javaConfiguration.getRootLogicalFilterComponent().add(createGradePropertyFilter(dataLoader));
    }

    protected PropertyFilter<Customer> createCustomerPropertyFilter(DataLoader dataLoader) {
        PropertyFilter<Customer> customerPropertyFilter = uiComponents.create(PropertyFilter.class);

        customerPropertyFilter.setConditionModificationDelegated(true);
        customerPropertyFilter.setDataLoader(dataLoader);
        customerPropertyFilter.setProperty("customer");
        customerPropertyFilter.setOperation(PropertyFilter.Operation.EQUAL);
        customerPropertyFilter.setOperationEditable(true);

        customerPropertyFilter.setParameterName(PropertyConditionUtils.generateParameterName(
                customerPropertyFilter.getProperty()));
        customerPropertyFilter.setValueComponent(singleFilterSupport.generateValueComponent(
                dataLoader.getContainer().getEntityMetaClass(),
                customerPropertyFilter.getProperty(),
                customerPropertyFilter.getOperation()
        ));

        return customerPropertyFilter;
    }

    protected PropertyFilter<CustomerGrade> createGradePropertyFilter(DataLoader dataLoader) {
        PropertyFilter<CustomerGrade> gradePropertyFilter = uiComponents.create(PropertyFilter.class);
        gradePropertyFilter.setConditionModificationDelegated(true);
        gradePropertyFilter.setDataLoader(dataLoader);
        gradePropertyFilter.setProperty("customer.grade");
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


