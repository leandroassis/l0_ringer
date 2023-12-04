/*
* Laboratório de Processamento de Sinais - LPS (UFRJ)
* Projeto: L0Ringer
* Data: 04/12/2023
* Autor: Leandro Assis dos Santos
* Descrição: Módulo responsável por construir as torres de energia para cada camada com os dados de eventos lidos da memória
*/

module tower_builder (top_addr, bottom_addr, towers, event_done);

    # (
    parameter MEMORY_ADDR_LENGTH = 20;

    // confirmar arquitetura lorenzetti
    parameter NUM_LAYERS = 8; 
    parameter TOWER_DETA = 0.1, TOWER_DPHI = 0.1;
    parameter MIN_ETA = -3.0, MAX_ETA = 3.0, MIN_PHI = -3.0, MAX_PHI = 3.0;
    )

    integer NUM_TOWERS_ETA = (MAX_ETA - MIN_ETA) / TOWER_DETA;
    integer NUM_TOWERS_PHI = (MAX_PHI - MIN_PHI) / TOWER_DPHI;

    typedef reg [NUM_TOWERS_ETA-1:0][(NUM_TOWERS_PHI-1):0] tower;

    input [MEMORY_ADDR_LENGTH-1:0] top_addr, bottom_addr;
    output tower [NUM_LAYERS-1:0] towers ;

    output event_done;

endmodule;