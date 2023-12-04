/*
* Laboratório de Processamento de Sinais - LPS (UFRJ)
* Projeto: L0Ringer
* Data: 04/12/2023
* Autor: Leandro Assis dos Santos
* Descrição: Módulo responsável por construir as torres de energia para cada camada com os dados de eventos lidos da memória
*/

module tower_builder (top_addr, bottom_addr, towers, event_done);

    parameter memory_addr_length = 20;

    // confirmar arquitetura lorenzetti
    parameter num_layers = 8; 
    parameter tower_deta = 0.1, tower_dphi = 0.1;
    parameter min_eta = -3.0, max_eta = 3.0, min_phi = -3.0, max_phi = 3.0;

    parameter num_towers_eta = (max_eta - min_eta) / tower_deta;
    parameter num_towers_phi = (max_phi - min_phi) / tower_dphi;

    input [(memory_addr-1):0] top_addr, bottom_addr;
    output [(num_layers-1):0] towers [(num_towers_eta-1):0][(num_towers_phi-1):0];

    output event_done; // bit que indica que o evento foi lido da memória

endmodule;