package com.selimhorri.app.e2e;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.selimhorri.app.dto.PaymentDto;
import com.selimhorri.app.domain.PaymentStatus;
import com.selimhorri.app.dto.OrderDto;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class PaymentE2ETest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldCreatePaymentAndReturn200() throws Exception {
        PaymentDto paymentDto = PaymentDto.builder()
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .orderDto(OrderDto.builder().orderId(1).build())
                .build();

        mockMvc.perform(post("/api/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(paymentDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.isPayed").value(true))
                .andExpect(jsonPath("$.paymentStatus").value("COMPLETED"));
    }


    @Test
    void shouldUpdatePaymentAndReturn200() throws Exception {
        // Primero crea un pago
        PaymentDto paymentDto = PaymentDto.builder()
                .isPayed(false)
                .paymentStatus(PaymentStatus.IN_PROGRESS)
                .orderDto(OrderDto.builder().orderId(3).build())
                .build();

        String createResponse = mockMvc.perform(post("/api/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(paymentDto)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        PaymentDto createdPayment = objectMapper.readValue(createResponse, PaymentDto.class);

        // Actualiza el pago
        createdPayment.setIsPayed(true);
        createdPayment.setPaymentStatus(PaymentStatus.COMPLETED);

        mockMvc.perform(put("/api/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(createdPayment)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.isPayed").value(true))
                .andExpect(jsonPath("$.paymentStatus").value("COMPLETED"));
    }

    @Test
    void shouldDeletePaymentAndReturn200() throws Exception {
        // Primero crea un pago
        PaymentDto paymentDto = PaymentDto.builder()
                .isPayed(true)
                .paymentStatus(PaymentStatus.COMPLETED)
                .orderDto(OrderDto.builder().orderId(4).build())
                .build();

        String createResponse = mockMvc.perform(post("/api/payments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(paymentDto)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        PaymentDto createdPayment = objectMapper.readValue(createResponse, PaymentDto.class);

        // Elimina el pago
        mockMvc.perform(delete("/api/payments/" + createdPayment.getPaymentId()))
                .andExpect(status().isOk())
                .andExpect(content().string("true"));
    }

}