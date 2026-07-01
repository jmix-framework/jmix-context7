<Path>Components > EntityComboBox > EntityComboBox with items fetch callback</Path>

EntityComboBox component supports a callback for fetching items from a back end: You can define the query declaratively using itemsQuery element in XML. The itemsQuery element for the EntityComboBox has following attributes: class (required) - a full qualified name of an entity class. fetchPlan - an optional attribute that specifies the fetch plan to be used for loading the queried entity. escapeValueForLike - enables searching for the values that contain special symbols: %, \, etc. The default value is false. searchStringFormat - a string that contains a variable to be substituted with actual value by io.jmix.flowui.sys.substitutor.StringSubstitutor. The default implementation delegates its work to org.apache.commons.text.StringSubstitutor.. The itemsQuery element for the EntityComboBox has the following nested elements: query - an element that contains a JPQL query. fetchPlan - an optional descriptor of inline fetch plan. If itemsQuery is not defined, you can programmatically set the list of options using setItemsFetchCallback in the ViewController. Note: Because the real work is delegated tocom.vaadin.flow.data.provider.HasLazyDataView#setItems(com.vaadin.flow.data.provider.CallbackDataProvider.FetchCallback, the QueryTrace instance is passed to the fetch callback. As a result, there are several limitations: query.getOffset() and query.getLimit() methods must be called, otherwise an exception is thrown. The amount of items returned from callback cannot exceed the limit value, otherwise an exception is thrown.

entity-combobox-items-query.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%">
            <tab id="declarativeTab" label="Declaratively">
                <entityComboBox id="declarativeEntityComboBox" label="Customer"
                                metaClass="Customer">
                    <actions>
                        <action id="entityLookup" type="entity_lookup"/>
                        <action id="entityClear" type="entity_clear"/>
                    </actions>
                    <itemsQuery class="io.jmix.uisamples.entity.Customer"
                                searchStringFormat="(?i)%${inputString}%"
                                escapeValueForLike="true"
                                fetchPlan="_local">
                        <query>
                            <![CDATA[select e from Customer e where e.name
                            like :searchString escape '\' order by e.name asc]]>
                        </query>
                    </itemsQuery>
                </entityComboBox>
            </tab>
            <tab id="programmaticTab" label="Programmatic">
                <entityComboBox id="programmaticEntityComboBox" label="Customer"
                                metaClass="Customer">
                    <actions>
                        <action id="entityLookup" type="entity_lookup"/>
                        <action id="entityClear" type="entity_clear"/>
                    </actions>
                </entityComboBox>
            </tab>
        </tabSheet>
    </layout>
</view>




EntityComboBoxItemsQuery.java

package io.jmix.uisamples.view.flowui.components.entitycombobox.itemsquery;

import com.vaadin.flow.data.provider.Query;
import io.jmix.core.DataManager;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.stream.Stream;

@ViewController("entity-combobox-items-query")
@ViewDescriptor("entity-combobox-items-query.xml")
public class EntityComboBoxItemsQuery extends StandardView {

    @Autowired
    protected DataManager dataManager;

    protected Collection<Customer> customers;

    @Subscribe
    protected void onInit(InitEvent event) {
        customers = dataManager.load(Customer.class).all().list();
    }

    @Install(to = "programmaticEntityComboBox", subject = "itemsFetchCallback")
    protected Stream<Customer> programmaticEntityComboBoxItemsFetchCallback(Query<Customer, String> query) {
        String enteredValue = query.getFilter()
                .orElse("");

        return customers.stream()
                .filter(customer -> customer.getName() != null &&
                        customer.getName().toLowerCase().contains(enteredValue.toLowerCase()))
                .skip(query.getOffset())
                .limit(query.getLimit());
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


