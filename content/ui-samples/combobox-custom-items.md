<Path>Components > ComboBox > ComboBox with custom items</Path>

The list of ComboBox items can be specified using the following methods: setItems() - allows you to specify programmatically component items; ComponentUtils.setItemsMap() - allows you to specify a string label for each item value explicitly; The placeholder attribute allow you to specify a string to display the empty value.

combobox-custom-items.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="orderDc"
                  class="io.jmix.uisamples.entity.Order"
                  fetchPlan="_local"/>
        <instance id="customerDc"
                  class="io.jmix.uisamples.entity.Customer"
                  fetchPlan="_local"/>
    </data>
    <layout classNames="horizontal-layout">
        <comboBox id="amountComboBox"
                  label="Items List"
                  dataContainer="orderDc"
                  property="amount"/>
        <comboBox id="ageComboBox"
                  label="Items Map"
                  dataContainer="customerDc"
                  property="age"/>
        <comboBox id="gradeComboBox"
                  label="Items Enum"
                  dataContainer="customerDc"
                  itemsEnum="io.jmix.uisamples.entity.CustomerGrade"
                  property="grade"
                  placeholder="Select grade"/>
    </layout>
</view>




ComboBoxCustomItemsSample.java

package io.jmix.uisamples.view.flowui.components.combobox.customitems;

import io.jmix.core.Metadata;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.Order;
import org.springframework.beans.factory.annotation.Autowired;

import java.math.BigDecimal;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@ViewController("combobox-custom-items")
@ViewDescriptor("combobox-custom-items.xml")
public class ComboBoxCustomItemsSample extends StandardView {

    @ViewComponent
    protected JmixComboBox<Integer> ageComboBox;
    @ViewComponent
    protected JmixComboBox<BigDecimal> amountComboBox;

    @ViewComponent
    protected InstanceContainer<Customer> customerDc;
    @ViewComponent
    protected InstanceContainer<Order> orderDc;

    @Autowired
    protected Metadata metadata;
    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        // InstanceContainer initialization. It is usually done automatically if the view is
        // inherited from StandardDetailView and is used as an entity detail.
        Order order = metadata.create(Order.class);
        orderDc.setItem(order);

        Customer customer = metadata.create(Customer.class);
        customerDc.setItem(customer);

        amountComboBox.setItems(getAmountItemsList());
        ComponentUtils.setItemsMap(ageComboBox, getAgeItemsMap());
    }

    protected List<BigDecimal> getAmountItemsList() {
        return List.of(
                BigDecimal.valueOf(1000),
                BigDecimal.valueOf(2000),
                BigDecimal.valueOf(3000),
                BigDecimal.valueOf(4000)
        );
    }

    protected Map<Integer, String> getAgeItemsMap() {
        LinkedHashMap<Integer, String> map = new LinkedHashMap<>();
        map.put(20, "Twenty");
        map.put(30, "Thirty");
        map.put(40, "Forty");
        map.put(50, "Fifty");
        return map;
    }

    @Subscribe(id = "orderDc", target = Target.DATA_CONTAINER)
    protected void onOrderDcItemPropertyChange(InstanceContainer.ItemPropertyChangeEvent<Order> event) {
        itemPropertyChanged(event);
    }

    @Subscribe(id = "customerDc", target = Target.DATA_CONTAINER)
    protected void onCustomerDcItemPropertyChange(InstanceContainer.ItemPropertyChangeEvent<Customer> event) {
        itemPropertyChanged(event);
    }

    protected void itemPropertyChanged(InstanceContainer.ItemPropertyChangeEvent<?> event) {
        String message = event.getItem().getClass().getSimpleName()
                + "." + event.getProperty()
                + " = " + event.getValue();
        notifications.show(message);
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


